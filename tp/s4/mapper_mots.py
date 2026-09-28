#!/usr/bin/env python3
"""Mapper : émet « mot<TAB>1 » pour chaque mot des avis clients.

Entrée : note<TAB>langue<TAB>texte, par exemple
    5	darija	wsalni casque f yumayn, lkhedma zwina.
Règles : passer le texte en minuscules, garder les suites de lettres (accents
compris) et de chiffres (l'arabizi écrit certains sons avec 3, 7, 9), et ne
garder que les mots d'au moins 2 caractères. L'expression régulière MOT est
fournie.
C'est le « word count », l'exemple historique de MapReduce, et la première
étape de toute préparation de texte pour un modèle de langue.
"""
import re
import sys

sys.stdin.reconfigure(encoding="utf-8", errors="replace")
sys.stdout.reconfigure(encoding="utf-8")

MOT = re.compile(r"[a-z0-9à-öø-ÿ]+")

for ligne in sys.stdin:
    # TODO 1 : découper la ligne sur les tabulations ; ignorer si pas 3 morceaux
    # TODO 2 : pour chaque mot de MOT.findall(texte.lower()) d'au moins 2 caractères,
    #          afficher « mot<TAB>1 »
    pass
