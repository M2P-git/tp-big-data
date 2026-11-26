"""S7 : simulateurs pédagogiques déterministes, sans base ni réseau réels.

    python tp/s7/s7_demo.py placement
    python tp/s7/s7_demo.py panne
    python tp/s7/s7_demo.py cap
    python tp/s7/s7_demo.py quorum
"""
import argparse
import hashlib
import itertools
import json
from copy import deepcopy


class Indisponible(Exception):
    pass


class ClusterPedagogique:
    """Placement fixe par modulo, puis copies sur les noeuds suivants.

    Les pannes ne changent pas le placement. Pas de réseau, de migration,
    de détection de panne ou de consensus réels dans ce modèle.
    """
    def __init__(self, noeuds=('A','B','C','D'), copies=2):
        if not noeuds or len(set(noeuds)) != len(noeuds):
            raise ValueError('Les noeuds doivent être distincts et non vides.')
        if not 1 <= copies <= len(noeuds):
            raise ValueError('Le nombre de copies doit être compris entre 1 et N.')
        self.noeuds = tuple(noeuds)
        self.copies = copies
        self.actifs = set(noeuds)
        self.stock = {n:{} for n in noeuds}

    def proprietaires(self, cle):
        h = int.from_bytes(hashlib.sha256(cle.encode('utf-8')).digest()[:4], 'big')
        debut = h % len(self.noeuds)
        return tuple(self.noeuds[(debut+i) % len(self.noeuds)] for i in range(self.copies))

    def put(self, cle, valeur):
        copies = self.proprietaires(cle)
        if any(n not in self.actifs for n in copies):
            raise Indisponible('Le chargement pédagogique exige toutes les copies actives.')
        for n in copies:
            self.stock[n][cle] = deepcopy(valeur)

    def get(self, cle):
        for n in self.proprietaires(cle):
            if n in self.actifs and cle in self.stock[n]:
                return deepcopy(self.stock[n][cle])
        raise Indisponible(f'Aucune copie accessible pour {cle}.')

    def arreter(self, noeud):
        if noeud not in self.stock:
            raise ValueError('Noeud inconnu.')
        self.actifs.discard(noeud)

    def distribution(self):
        return {n:len(d) for n,d in self.stock.items()}


def charger_demo(copies=2):
    c = ClusterPedagogique(copies=copies)
    for identifiant in range(101,113):
        c.put(f'panier:{identifiant}', {'produit':'1001','quantite':1})
    return c


def scenario_cap(politique):
    """Chronologie illustrative, un seul écrivain, deux répliques isolées.

    Deux choix conceptuels pour la lecture sur B après une écriture achevée
    sur A. Ce scénario n'implémente aucun protocole CP/AP de production.
    """
    if politique not in ('coherence','reponse_locale'):
        raise ValueError('Politique inconnue.')
    return [
        {'etape':'initial','A':10,'B':10,'lecture_B':10},
        {'etape':'liaison coupee','A':10,'B':10,
         'lecture_B':'indisponible' if politique=='coherence' else 10},
        {'etape':'ecriture sur A terminee','A':9,'B':10,
         'lecture_B':'indisponible' if politique=='coherence' else 10},
        {'etape':'liaison retablie et copie propagee','A':9,'B':9,'lecture_B':9},
    ]


def intersections(n, r, w):
    if n < 1 or not (1 <= r <= n and 1 <= w <= n):
        raise ValueError('N, R et W doivent décrire des ensembles possibles.')
    noeuds = range(n)
    return [set(lecture)&set(ecriture)
            for lecture in itertools.combinations(noeuds,r)
            for ecriture in itertools.combinations(noeuds,w)]


def verifier():
    c = charger_demo()
    assert sum(c.distribution().values()) == 24
    assert all(len(set(c.proprietaires(f'panier:{i}')))==2 for i in range(101,113))
    c.arreter('A')
    assert all(c.get(f'panier:{i}')['quantite']==1 for i in range(101,113))
    cle='panier:101'
    avant=c.proprietaires(cle)
    for n in avant: c.arreter(n)
    assert c.proprietaires(cle)==avant
    try: c.get(cle)
    except Indisponible: pass
    else: raise AssertionError('Deux copies inaccessibles devaient bloquer la lecture.')
    assert scenario_cap('coherence')[2]['lecture_B']=='indisponible'
    assert scenario_cap('reponse_locale')[2]['lecture_B']==10
    assert scenario_cap('reponse_locale')[-1]['lecture_B']==9
    assert all(intersections(3,2,2))
    assert not all(intersections(3,1,1))
    print('OK : placement, copies distinctes, panne, chronologie CAP et intersections.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['placement','panne','cap','quorum','verifier','tout'])
    a=p.parse_args()
    if a.mode in ('placement','tout'):
        c=charger_demo()
        print('12 clés logiques, 2 copies par clé, 24 placements.')
        print('Clé panier:101 :', ', '.join(c.proprietaires('panier:101')))
        print('Copies stockées par noeud :',c.distribution())
    if a.mode in ('panne','tout'):
        c=charger_demo()
        c.arreter('A')
        print('A arrêté :',sum(c.get(f'panier:{i}') is not None for i in range(101,113)),'clés encore lisibles.')
        cle='panier:101'
        for n in c.proprietaires(cle): c.arreter(n)
        try: c.get(cle)
        except Indisponible as e: print(e)
    if a.mode in ('cap','tout'):
        for politique in ('coherence','reponse_locale'):
            print(politique)
            for ligne in scenario_cap(politique): print(json.dumps(ligne,ensure_ascii=False))
    if a.mode in ('quorum','tout'):
        for r,w in [(1,1),(2,2),(3,1)]:
            tous=intersections(3,r,w)
            print(f'N=3, R={r}, W={w} : intersection minimale = {min(map(len,tous))}')
        print('Une intersection ne prouve pas à elle seule la linéarisabilité.')
    if a.mode in ('verifier','tout'): verifier()


if __name__=='__main__': main()
