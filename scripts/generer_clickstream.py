#!/usr/bin/env python3
"""Génère un clickstream synthétique de Qissaria au format du jeu REES46.

Colonnes (identiques au jeu public REES46 publié sur Kaggle) :
    event_time, event_type, product_id, category_id, category_code,
    brand, price, user_id, user_session

Les événements sont regroupés en sessions cohérentes (des vues, parfois un
ajout au panier, parfois un achat du produit mis au panier) et le fichier est
trié par date, jour après jour, comme un vrai journal de site marchand.

Exemples :
    python generer_clickstream.py --lignes 5000 --sortie ../data/echantillon/clickstream_echantillon.csv
    python generer_clickstream.py --taille 1.5G --sortie ../data/clickstream_aout.csv

Aucune dépendance externe : Python 3.9 ou plus suffit.
"""

from __future__ import annotations

import argparse
import datetime as dt
import random
import sys
import time

EN_TETE = ("event_time,event_type,product_id,category_id,category_code,"
           "brand,price,user_id,user_session\n")

# (category_code, poids de la catégorie, prix minimal, prix maximal)
CATEGORIES = [
    ("electronics.smartphone", 22, 900, 14000),
    ("electronics.audio.headphone", 6, 90, 2500),
    ("electronics.video.tv", 5, 1800, 16000),
    ("computers.notebook", 6, 3500, 22000),
    ("computers.peripherals.mouse", 3, 40, 600),
    ("appliances.kitchen.refrigerators", 4, 2800, 15000),
    ("appliances.kitchen.washer", 4, 2500, 9000),
    ("appliances.kitchen.teapot", 3, 60, 700),
    ("apparel.shoes", 7, 150, 1500),
    ("apparel.djellaba", 4, 250, 3000),
    ("furniture.living_room.sofa", 3, 2500, 18000),
    ("home.decor.carpet", 4, 400, 9000),
    ("home.decor.lamp", 3, 120, 1800),
    ("kids.toys", 5, 50, 900),
    ("beauty.argan_oil", 4, 40, 400),
    ("food.olive_oil", 3, 45, 250),
    ("food.dates", 3, 30, 300),
    ("sport.bicycle", 2, 1200, 9000),
    ("", 9, 20, 800),  # produits sans catégorie renseignée, comme dans REES46
]

MARQUES = [
    "atlas", "zellij", "nakhla", "sahara", "medina", "argana", "oasis",
    "rif", "tafilalt", "mogador", "novatek", "kora", "lumio", "vexa",
    "orbita", "dunes", "kasbah", "safran", "tidra", "noria",
]

# Poids horaires (0 h à 23 h) : creux la nuit, pic en soirée.
POIDS_HEURES = [2, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 6,
                6, 6, 5, 5, 6, 7, 8, 9, 10, 10, 8, 4]

OCTETS_MOYENS_PAR_LIGNE = 137  # estimation pour convertir une taille en lignes


def lire_taille(texte: str) -> int:
    """Convertit '500M', '1.5G' ou '2000000' en nombre d'octets."""
    texte = texte.strip().upper()
    facteurs = {"K": 10**3, "M": 10**6, "G": 10**9, "T": 10**12}
    if texte[-1] in facteurs:
        return int(float(texte[:-1]) * facteurs[texte[-1]])
    return int(texte)


def construire_catalogue(rng: random.Random, nb_produits: int):
    """Crée un catalogue de produits regroupés par catégorie."""
    total = sum(c[1] for c in CATEGORIES)
    catalogue = []  # liste de listes de produits, une par catégorie
    prochain_id = 1000000
    for code, poids, pmin, pmax in CATEGORIES:
        n = max(20, nb_produits * poids // total)
        category_id = 2053013550000000000 + rng.randrange(10**12)
        produits = []
        for _ in range(n):
            marque = "" if rng.random() < 0.12 else rng.choice(MARQUES)
            prix = round(rng.uniform(pmin, pmax), 2)
            produits.append((str(prochain_id), str(category_id), code, marque,
                             f"{prix:.2f}"))
            prochain_id += rng.randrange(1, 40)
        catalogue.append(produits)
    poids_categories = [c[1] for c in CATEGORIES]
    return catalogue, poids_categories


def choisir_zipf(rng: random.Random, n: int) -> int:
    """Indice entre 0 et n-1, les premiers indices étant bien plus fréquents."""
    return min(n - 1, int(n * rng.random() ** 3))


def generer_jour(rng, jour, nb_sessions, catalogue, poids_categories,
                 nb_clients):
    """Renvoie les lignes CSV d'une journée, triées par horodatage."""
    evenements = []
    minuit = dt.datetime(jour.year, jour.month, jour.day)
    heures = rng.choices(range(24), weights=POIDS_HEURES, k=nb_sessions)
    for heure in heures:
        user_id = str(512000000 + choisir_zipf(rng, nb_clients))
        session = "%032x" % rng.getrandbits(128)
        session = (f"{session[:8]}-{session[8:12]}-{session[12:16]}-"
                   f"{session[16:20]}-{session[20:]}")
        t = minuit + dt.timedelta(hours=heure,
                                  seconds=rng.randrange(3600))
        idx_cat = rng.choices(range(len(catalogue)),
                              weights=poids_categories)[0]
        # Longueur de session : loi géométrique de moyenne 7 environ.
        longueur = 1
        while rng.random() < 0.86 and longueur < 60:
            longueur += 1
        panier = []
        for _ in range(longueur):
            if rng.random() < 0.8:
                produits = catalogue[idx_cat]
            else:
                produits = catalogue[rng.randrange(len(catalogue))]
            produit = produits[choisir_zipf(rng, len(produits))]
            evenements.append((t, "view", produit, user_id, session))
            if rng.random() < 0.05:
                t += dt.timedelta(seconds=rng.randrange(3, 40))
                evenements.append((t, "cart", produit, user_id, session))
                panier.append(produit)
            t += dt.timedelta(seconds=rng.randrange(5, 150))
        for produit in panier:
            if rng.random() < 0.35:
                t += dt.timedelta(seconds=rng.randrange(20, 300))
                evenements.append((t, "purchase", produit, user_id, session))
    evenements.sort(key=lambda e: e[0])
    lignes = []
    for t, type_evt, (pid, cid, code, marque, prix), user_id, session in evenements:
        if t.date() != jour:  # une session qui déborde après minuit est coupée
            continue
        lignes.append(f"{t:%Y-%m-%d %H:%M:%S} UTC,{type_evt},{pid},{cid},"
                      f"{code},{marque},{prix},{user_id},{session}\n")
    return lignes


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    groupe = parser.add_mutually_exclusive_group(required=True)
    groupe.add_argument("--lignes", type=int, help="nombre de lignes voulu")
    groupe.add_argument("--taille", type=str,
                        help="taille visée du fichier, par exemple 500M ou 1.5G")
    parser.add_argument("--sortie", required=True, help="fichier CSV produit")
    parser.add_argument("--debut", default="2026-08-01",
                        help="premier jour (AAAA-MM-JJ), 2026-08-01 par défaut")
    parser.add_argument("--jours", type=int, default=31,
                        help="nombre de jours couverts (31 par défaut)")
    parser.add_argument("--produits", type=int, default=40000,
                        help="taille du catalogue (40000 par défaut)")
    parser.add_argument("--clients", type=int, default=300000,
                        help="nombre de clients distincts (300000 par défaut)")
    parser.add_argument("--graine", type=int, default=2026,
                        help="graine aléatoire, pour des fichiers reproductibles")
    args = parser.parse_args(argv)

    rng = random.Random(args.graine)
    catalogue, poids_categories = construire_catalogue(rng, args.produits)
    if args.lignes is not None:
        cible_lignes = args.lignes
        cible_octets = None
    else:
        cible_octets = lire_taille(args.taille)
        cible_lignes = cible_octets // OCTETS_MOYENS_PAR_LIGNE
    # Une session produit environ 7,5 lignes en moyenne.
    sessions_par_jour = max(1, int(cible_lignes / 7.5 / args.jours * 1.05))

    debut = dt.date.fromisoformat(args.debut)
    ecrites = 0
    octets = len(EN_TETE)
    chrono = time.time()
    with open(args.sortie, "w", encoding="utf-8", newline="") as f:
        f.write(EN_TETE)
        jour_idx = 0
        while True:
            jour = debut + dt.timedelta(days=jour_idx)
            lignes = generer_jour(rng, jour, sessions_par_jour, catalogue,
                                  poids_categories, args.clients)
            for ligne in lignes:
                if cible_octets is None and ecrites >= cible_lignes:
                    break
                if cible_octets is not None and octets >= cible_octets:
                    break
                f.write(ligne)
                ecrites += 1
                octets += len(ligne)
            else:
                jour_idx += 1
                print(f"\r{jour}  {ecrites:>12,} lignes  {octets / 1e6:>9.1f} Mo",
                      end="", file=sys.stderr)
                continue
            break
    duree = time.time() - chrono
    print(f"\nTerminé : {ecrites:,} lignes, {octets / 1e6:.1f} Mo en {duree:.0f} s"
          f" -> {args.sortie}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
