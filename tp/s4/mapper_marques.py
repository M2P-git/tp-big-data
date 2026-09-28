#!/usr/bin/env python3
"""Mapper : émet « marque<TAB>1 » pour chaque ACHAT dont la marque est renseignée.

Question de Salma : « Quelles sont les 10 marques les plus achetées ce mois-ci ? »
Rappel des colonnes :
    0 event_time, 1 event_type, 2 product_id, 3 category_id, 4 category_code,
    5 brand, 6 price, 7 user_id, 8 user_session
Le reducer à utiliser est reducer_somme.py : pas besoin d'en écrire un autre.
"""
import sys

sys.stdin.reconfigure(encoding="utf-8", errors="replace")
sys.stdout.reconfigure(encoding="utf-8")

for ligne in sys.stdin:
    # TODO : même début que mapper_evenements.py, puis n'émettre que les lignes
    #        dont event_type vaut "purchase" et dont la marque n'est pas vide
    pass
