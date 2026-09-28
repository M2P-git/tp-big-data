#!/usr/bin/env python3
"""Reducer : additionne les valeurs de chaque clé.

Entrée (stdin) : des lignes « clé<TAB>valeur » TRIÉES par clé, par exemple
    cart	1
    cart	1
    purchase	1
    view	1
Sortie (stdout) : une ligne par clé avec le total, par exemple
    cart	2
    purchase	1
    view	1

Idée : comme l'entrée est triée, toutes les lignes d'une même clé se suivent.
On garde la clé en cours et son total ; quand la clé change, on affiche le total.
"""
import sys

sys.stdin.reconfigure(encoding="utf-8", errors="replace")
sys.stdout.reconfigure(encoding="utf-8")

cle_courante, total = None, 0
for ligne in sys.stdin:
    cle, _, valeur = ligne.rstrip("\n").partition("\t")
    # TODO 1 : si la clé change (et qu'il y avait déjà une clé en cours),
    #          afficher « cle_courante<TAB>total », puis repartir de zéro
    # TODO 2 : ajouter int(valeur) au total
    pass

# TODO 3 : ne pas oublier d'afficher la dernière clé à la fin de la boucle
