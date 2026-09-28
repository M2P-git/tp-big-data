#!/usr/bin/env python3
"""Simule un job Hadoop Streaming sur votre machine, phase par phase.

Le script fait exactement ce que fait Hadoop, en petit :
  1. découpe l'entrée en blocs (splits) ;
  2. lance le mapper sur chaque bloc ;
  3. (option) lance un combiner sur la sortie de chaque mapper ;
  4. répartit les couples (clé, valeur) entre les reducers (partitionnement
     par hachage de la clé), puis trie chaque partition par clé (shuffle) ;
  5. lance le reducer sur chaque partition et écrit part-00000, part-00001...

Il affiche les volumes échangés à chaque étape : comparez avec et sans
combiner pour voir ce qu'il fait gagner au réseau.

Exemple (depuis le dossier tp/s4) :
    python simuler_mapreduce.py --entree ../../data/echantillon/clickstream_echantillon.csv \\
        --mapper mapper_evenements.py --reducer reducer_somme.py \\
        --splits 4 --reducers 2 --combiner reducer_somme.py
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import zlib


def executer(script: str, lignes: list[str]) -> list[str]:
    """Lance un script Python en lui passant des lignes sur l'entrée standard."""
    resultat = subprocess.run(
        [sys.executable, script],
        input="".join(lignes),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if resultat.returncode != 0:
        print(resultat.stderr, file=sys.stderr)
        raise SystemExit(f"Erreur dans {script} (code {resultat.returncode})")
    return resultat.stdout.splitlines(keepends=True)


def cle_de(ligne: str) -> str:
    return ligne.split("\t", 1)[0]


def partition(cle: str, nb_reducers: int) -> int:
    """Même idée que le HashPartitioner de Hadoop : hachage de la clé modulo R."""
    return zlib.crc32(cle.encode("utf-8")) % nb_reducers


def octets(lignes: list[str]) -> int:
    return sum(len(l.encode("utf-8")) for l in lignes)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--entree", required=True, help="fichier texte ou CSV")
    p.add_argument("--mapper", required=True)
    p.add_argument("--reducer", required=True)
    p.add_argument("--combiner", help="script de combiner (optionnel)")
    p.add_argument("--splits", type=int, default=4, help="nombre de blocs d'entrée")
    p.add_argument("--reducers", type=int, default=2, help="nombre de reducers")
    p.add_argument("--sortie", default="sortie_simulation",
                   help="dossier de sortie (part-00000...)")
    p.add_argument("--verbeux", action="store_true",
                   help="affiche un extrait de chaque étape")
    args = p.parse_args(argv)

    with open(args.entree, encoding="utf-8") as f:
        lignes = f.readlines()
    taille = -(-len(lignes) // args.splits)  # division arrondie au-dessus
    blocs = [lignes[i:i + taille] for i in range(0, len(lignes), taille)]
    print(f"[entrée]   {len(lignes):>9,} lignes, {octets(lignes):>11,} octets, "
          f"{len(blocs)} blocs")

    # Phase map (+ combiner éventuel), bloc par bloc
    sorties_map = []
    total_map, total_envoye = 0, 0
    for i, bloc in enumerate(blocs):
        sortie = executer(args.mapper, bloc)
        total_map += len(sortie)
        if args.combiner:
            sortie = executer(args.combiner, sorted(sortie, key=cle_de))
        total_envoye += octets(sortie)
        sorties_map.append(sortie)
        if args.verbeux:
            print(f"  map {i}: {len(bloc)} lignes lues -> {len(sortie)} couples, "
                  f"ex. {sortie[:2]}")
    print(f"[map]      {total_map:>9,} couples (clé, valeur) produits")
    if args.combiner:
        nb = sum(len(s) for s in sorties_map)
        print(f"[combiner] {nb:>9,} couples après combinaison locale")
    print(f"[shuffle]  {total_envoye:>9,} octets envoyés sur le réseau")

    # Phase shuffle : partitionnement puis tri par clé
    partitions = [[] for _ in range(args.reducers)]
    for sortie in sorties_map:
        for ligne in sortie:
            partitions[partition(cle_de(ligne), args.reducers)].append(ligne)
    for part in partitions:
        part.sort(key=cle_de)

    # Phase reduce
    os.makedirs(args.sortie, exist_ok=True)
    for r, part in enumerate(partitions):
        resultat = executer(args.reducer, part)
        chemin = os.path.join(args.sortie, f"part-{r:05d}")
        with open(chemin, "w", encoding="utf-8") as f:
            f.writelines(resultat)
        cles = len({cle_de(l) for l in part})
        print(f"[reduce {r}] {len(part):>7,} couples, {cles} clés -> {chemin} "
              f"({len(resultat)} lignes)")
        if args.verbeux:
            print("   ", "".join(resultat[:5]).replace("\n", " | "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
