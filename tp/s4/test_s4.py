"""Tests automatiques du TP S4.

Lancez-les depuis le dossier tp/s4 :
    python -m pytest -q

Chaque test fait tourner votre mapper puis votre reducer sur l'échantillon
(mapper | tri | reducer, comme Hadoop Streaming) et compare le résultat au
calcul fait directement en Python. Un test vert = un script juste.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ICI = Path(__file__).resolve().parent
DONNEES = ICI.parent.parent / "data" / "echantillon"
CLICKSTREAM = DONNEES / "clickstream_echantillon.csv"
AVIS = DONNEES / "avis_clients.tsv"


def pipeline(mapper: str, reducer: str, entree: Path) -> dict[str, int]:
    """Équivalent local de : cat entree | mapper | sort | reducer."""
    texte = entree.read_text(encoding="utf-8")
    sortie_map = subprocess.run([sys.executable, str(ICI / mapper)], input=texte,
                                capture_output=True, text=True, encoding="utf-8",
                                check=True).stdout
    triee = "".join(sorted(sortie_map.splitlines(keepends=True),
                           key=lambda l: l.split("\t", 1)[0]))
    sortie = subprocess.run([sys.executable, str(ICI / reducer)], input=triee,
                            capture_output=True, text=True, encoding="utf-8",
                            check=True).stdout
    resultat = {}
    for ligne in sortie.splitlines():
        cle, valeur = ligne.split("\t")
        assert cle not in resultat, f"clé {cle!r} émise deux fois par le reducer"
        resultat[cle] = int(valeur)
    return resultat


def lire_clickstream():
    with open(CLICKSTREAM, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_comptage_par_type_evenement():
    attendu = Counter(l["event_type"] for l in lire_clickstream())
    assert pipeline("mapper_evenements.py", "reducer_somme.py", CLICKSTREAM) == attendu


def test_achats_par_marque():
    attendu = Counter(l["brand"] for l in lire_clickstream()
                      if l["event_type"] == "purchase" and l["brand"])
    assert pipeline("mapper_marques.py", "reducer_somme.py", CLICKSTREAM) == attendu


def test_comptage_des_mots_des_avis():
    mot = re.compile(r"[a-z0-9à-öø-ÿ]+")
    attendu = Counter()
    for ligne in AVIS.read_text(encoding="utf-8").splitlines():
        texte = ligne.split("\t")[2]
        attendu.update(m for m in mot.findall(texte.lower()) if len(m) >= 2)
    assert pipeline("mapper_mots.py", "reducer_somme.py", AVIS) == attendu


def test_le_reducer_peut_servir_de_combiner():
    """Additionner des sommes partielles doit donner la même chose."""
    lignes = "a\t1\na\t1\nb\t1\n"
    partiel = subprocess.run([sys.executable, str(ICI / "reducer_somme.py")],
                             input=lignes, capture_output=True, text=True,
                             check=True).stdout
    assert partiel.splitlines() == ["a\t2", "b\t1"]
    # Un autre mapper a produit a=3 : Hadoop trie tout avant le reducer final
    triee = "".join(sorted((partiel + "a\t3\n").splitlines(keepends=True)))
    final = subprocess.run([sys.executable, str(ICI / "reducer_somme.py")],
                           input=triee, capture_output=True, text=True,
                           check=True).stdout
    assert final.splitlines() == ["a\t5", "b\t1"]


if __name__ == "__main__":
    # Sans pytest : python test_s4.py
    import traceback
    echecs = 0
    for nom, fonction in sorted(globals().items()):
        if nom.startswith("test_") and callable(fonction):
            try:
                fonction()
                print(f"OK     {nom}")
            except Exception:  # noqa: BLE001
                echecs += 1
                print(f"ECHEC  {nom}")
                traceback.print_exc(limit=1)
    print(f"\n{echecs} échec(s)")
    sys.exit(1 if echecs else 0)
