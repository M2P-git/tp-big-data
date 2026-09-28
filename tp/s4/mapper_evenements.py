#!/usr/bin/env python3
"""Mapper : émet « type_evenement<TAB>1 » pour chaque ligne du clickstream.

Entrée (stdin) : les lignes CSV du clickstream, par exemple
    2026-08-01 03:56:53 UTC,view,1779604,2053013838392686023,,,574.79,512066424,0f1a...
Sortie (stdout) : une ligne « clé<TAB>valeur » par événement, par exemple
    view	1

Testez en local :  python test_s4.py
"""
import sys

sys.stdin.reconfigure(encoding="utf-8", errors="replace")
sys.stdout.reconfigure(encoding="utf-8")

for ligne in sys.stdin:
    # TODO 1 : ignorer la ligne d'en-tête (elle commence par "event_time")
    # TODO 2 : découper la ligne sur les virgules ; ignorer les lignes qui n'ont pas 9 champs
    # TODO 3 : afficher le type d'événement (2e champ), une tabulation, puis 1
    pass
