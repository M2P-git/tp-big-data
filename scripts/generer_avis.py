#!/usr/bin/env python3
"""Génère des avis clients synthétiques de Qissaria (français, darija en arabizi, mélange).

Une ligne par avis, au format :  note<TAB>langue<TAB>texte

Les avis sont fabriqués à partir de gabarits : ils servent à compter des mots
(S4, MapReduce) puis à tester une analyse de sentiment (S11). Ce ne sont pas
de vrais avis.

Exemple :
    python generer_avis.py --nombre 2000 --sortie ../data/echantillon/avis_clients.tsv
"""

from __future__ import annotations

import argparse
import random
import sys

# (nom, avec article défini, avec démonstratif) : évite les fautes d'accord
PRODUITS = [
    ("téléphone", "le téléphone", "ce téléphone"),
    ("tapis", "le tapis", "ce tapis"),
    ("casque", "le casque", "ce casque"),
    ("frigo", "le frigo", "ce frigo"),
    ("lampe", "la lampe", "cette lampe"),
    ("djellaba", "la djellaba", "cette djellaba"),
    ("huile d'argan", "l'huile d'argan", "cette huile d'argan"),
    ("ordinateur", "l'ordinateur", "cet ordinateur"),
    ("vélo", "le vélo", "ce vélo"),
    ("théière", "la théière", "cette théière"),
    ("canapé", "le canapé", "ce canapé"),
    ("télé", "la télé", "cette télé"),
    ("jouet", "le jouet", "ce jouet"),
]

POSITIF_FR = [
    "Très bonne qualité pour {ce}, conforme à la description.",
    "Livraison rapide, reçu {le} en deux jours.",
    "Excellent rapport qualité prix pour {ce}.",
    "Je recommande {ce}, qualité au rendez-vous.",
    "Service client réactif, colis bien emballé pour {ce}.",
]
NEGATIF_FR = [
    "Livraison en retard et colis abîmé pour {ce}.",
    "{Le} ne correspond pas aux photos, déçu.",
    "Trop cher pour la qualité de {ce}.",
    "Panne après une semaine d'utilisation pour {ce}.",
    "Aucune réponse du service client au sujet de {ce}.",
]
POSITIF_DARIJA = [
    "sl3a mzyana bzaf, nsa7kom b Qissaria.",
    "wsalni {nom} f yumayn, lkhedma zwina.",
    "chrit {nom} w kolchi mzyan, taman mnasb.",
    "3jbatni lkhedma dyal Qissaria bzaf, chokran.",
]
NEGATIF_DARIJA = [
    "tsnnit {nom} simana kamla, khayba had lkhedma.",
    "chrit {nom} w kayn mochkil, bghit nrje3 flousi.",
    "taman ghali bzaf 3la had l9ualite.",
    "sl3a machi hiya li f tsawer, ma3jbatnich.",
]
MELANGE = [
    "Top {ce}, livraison rapide, mzyan bzaf.",
    "Franchement déçu, taman ghali w qualité moyenne.",
    "Bon produit mais tawsil t3ttel chwiya.",
    "Je recommande Qissaria, sl3a zwina.",
]


def generer(rng: random.Random):
    nom, le, ce = rng.choice(PRODUITS)
    tirage = rng.random()
    if tirage < 0.5:
        langue = "fr"
        positif = rng.random() < 0.6
        texte = rng.choice(POSITIF_FR if positif else NEGATIF_FR)
    elif tirage < 0.8:
        langue = "darija"
        positif = rng.random() < 0.6
        texte = rng.choice(POSITIF_DARIJA if positif else NEGATIF_DARIJA)
    else:
        langue = "mixte"
        positif = None
        texte = rng.choice(MELANGE)
    if positif is None:
        note = rng.randint(2, 5)
    elif positif:
        note = rng.choice([4, 5, 5])
    else:
        note = rng.choice([1, 1, 2])
    texte = texte.format(nom=nom, le=le, ce=ce, Le=le[0].upper() + le[1:])
    return note, langue, texte


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--nombre", type=int, default=2000)
    parser.add_argument("--sortie", required=True)
    parser.add_argument("--graine", type=int, default=2026)
    args = parser.parse_args(argv)
    rng = random.Random(args.graine)
    with open(args.sortie, "w", encoding="utf-8", newline="\n") as f:
        for _ in range(args.nombre):
            note, langue, texte = generer(rng)
            f.write(f"{note}\t{langue}\t{texte}\n")
    print(f"{args.nombre} avis -> {args.sortie}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
