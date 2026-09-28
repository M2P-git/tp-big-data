#!/usr/bin/env python3
"""Vérifie que votre poste est prêt pour les TP (à lancer depuis la racine du dépôt).

    python scripts/verifier_env.py             # avant de démarrer quoi que ce soit
    python scripts/verifier_env.py --cluster   # quand le profil hadoop tourne

Chaque ligne affiche OK, ATTENTION ou ECHEC avec la marche à suivre.
"""

from __future__ import annotations

import argparse
import re
import shutil
import socket
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
resultats = {"OK": 0, "ATTENTION": 0, "ECHEC": 0}


def dire(etat: str, message: str, conseil: str = "") -> None:
    resultats[etat] += 1
    print(f"[{etat:<9}] {message}")
    if conseil and etat != "OK":
        print(f"            -> {conseil}")


def lancer(commande: list[str], delai: int = 60) -> tuple[int, str]:
    try:
        r = subprocess.run(commande, capture_output=True, text=True, timeout=delai,
                           cwd=RACINE)
        return r.returncode, (r.stdout + r.stderr).strip()
    except FileNotFoundError:
        return 127, "commande introuvable"
    except subprocess.TimeoutExpired:
        return 124, "délai dépassé"


def verifier_poste() -> None:
    v = sys.version_info
    if v >= (3, 9):
        dire("OK", f"Python {v.major}.{v.minor}")
    else:
        dire("ECHEC", f"Python {v.major}.{v.minor} trop ancien", "installer Python 3.9 ou plus")

    code, sortie = lancer(["docker", "version", "--format", "{{.Server.Version}}"])
    if code == 0:
        dire("OK", f"Docker répond (moteur {sortie})")
    elif code == 127:
        dire("ECHEC", "Docker n'est pas installé", "installer Docker Desktop")
        return
    else:
        dire("ECHEC", "Docker est installé mais le moteur ne répond pas",
             "lancer Docker Desktop et attendre qu'il soit prêt")
        return

    code, sortie = lancer(["docker", "compose", "version", "--short"])
    dire("OK" if code == 0 else "ECHEC", f"Docker Compose {sortie if code == 0 else 'absent'}",
         "mettre à jour Docker Desktop")

    code, sortie = lancer(["docker", "info", "--format", "{{.MemTotal}}"])
    if code == 0 and sortie.isdigit():
        go = int(sortie) / 1024**3
        if go >= 5.5:
            dire("OK", f"Mémoire donnée à Docker : {go:.1f} Go")
        elif go >= 3.5:
            dire("ATTENTION", f"Mémoire donnée à Docker : {go:.1f} Go",
                 "ça passe pour un bloc à la fois ; fermer le navigateur pendant les TP Hadoop")
        else:
            dire("ECHEC", f"Mémoire donnée à Docker : {go:.1f} Go",
                 "augmenter la mémoire de WSL2 (.wslconfig) ou travailler en binôme")

    libre = shutil.disk_usage(RACINE).free / 1024**3
    etat = "OK" if libre >= 15 else ("ATTENTION" if libre >= 8 else "ECHEC")
    dire(etat, f"Espace disque libre : {libre:.0f} Go",
         "prévoir 15 Go (images Docker et données) : libérer de la place")

    code, sortie = lancer(["docker", "compose", "--profile", "socle", "--profile",
                           "hadoop", "config", "--quiet"])
    dire("OK" if code == 0 else "ECHEC", "compose.yaml valide",
         sortie.splitlines()[-1] if sortie else "")

    code, sortie = lancer(["docker", "image", "ls", "--format", "{{.Repository}}:{{.Tag}}"])
    images = set(sortie.split())
    for image in ["apache/hadoop:3.5.0", "quay.io/jupyter/pyspark-notebook:latest"]:
        dire("OK" if image in images else "ATTENTION", f"image {image}",
             "docker compose pull, ou docker load -i depuis la clé USB")

    for port, service in [(8888, "Jupyter"), (9870, "HDFS"), (8088, "YARN")]:
        with socket.socket() as s:
            libre = s.connect_ex(("127.0.0.1", port)) != 0
        dire("OK" if libre else "ATTENTION", f"port {port} ({service}) "
             f"{'libre' if libre else 'déjà utilisé'}",
             "normal si le service tourne déjà ; sinon fermer le programme qui l'occupe")

    echantillon = RACINE / "data" / "echantillon" / "clickstream_echantillon.csv"
    dire("OK" if echantillon.exists() else "ECHEC", "échantillon de données présent",
         "refaire git pull, ou relancer scripts/generer_clickstream.py")


def verifier_cluster() -> None:
    code, sortie = lancer(["docker", "compose", "exec", "-T", "namenode",
                           "hdfs", "dfsadmin", "-report"], delai=90)
    if code != 0:
        dire("ECHEC", "le NameNode ne répond pas",
             "docker compose --profile hadoop up -d, puis attendre 30 s")
        return
    vivants = re.search(r"Live datanodes \((\d+)\)", sortie)
    n = int(vivants.group(1)) if vivants else 0
    dire("OK" if n >= 3 else "ECHEC", f"{n} DataNode(s) vivant(s)",
         "attendre 30 s puis relancer ; sinon docker compose logs datanode")
    code, sortie = lancer(["docker", "compose", "exec", "-T", "resourcemanager",
                           "yarn", "node", "-list"], delai=90)
    actifs = re.search(r"Total Nodes:(\d+)", sortie)
    n = int(actifs.group(1)) if actifs else 0
    dire("OK" if n >= 1 else "ECHEC", f"{n} NodeManager(s) enregistré(s) auprès de YARN",
         "docker compose logs nodemanager")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cluster", action="store_true",
                        help="vérifier le cluster Hadoop en marche")
    args = parser.parse_args()
    print(f"Dépôt : {RACINE}\n")
    verifier_cluster() if args.cluster else verifier_poste()
    print(f"\nBilan : {resultats['OK']} OK, {resultats['ATTENTION']} attention, "
          f"{resultats['ECHEC']} échec(s)")
    return 1 if resultats["ECHEC"] else 0


if __name__ == "__main__":
    sys.exit(main())
