# Big Data et bases de données NoSQL : dépôt des TP

Module 1, cycle d'ingénieurs 3e année, filière intelligence artificielle (CI3 AI), année 2026-2027.
Enseignant : Dr Paul Menounga Mbilong.

Ce dépôt contient tout ce qu'il faut pour les manipulations : l'environnement Docker, les données de Qissaria (notre place de marché fictive), les notebooks et les scripts. Le cours lui-même est dans le support Quarto.

## Contenu (mois 1)

| Séance | Thème | Dossier | Environnement |
| --- | --- | --- | --- |
| S1 | Pourquoi le Big Data ? | [`tp/s1`](tp/s1) | papier, sans ordinateur |
| S2 | Une machine ne suffit plus | [`tp/s2`](tp/s2) | profil `socle` (Jupyter) |
| S3 | HDFS, stocker sur plusieurs machines | [`tp/s3`](tp/s3) | profil `hadoop` |
| S4 | MapReduce et YARN | [`tp/s4`](tp/s4) | profil `hadoop` |

```
.
├── compose.yaml            # tous les services, rangés par profils
├── hadoop/hadoop.env       # configuration du cluster Hadoop
├── data/                   # données (gros fichiers hors git) et échantillons
├── scripts/                # génération de données, vérification du poste
└── tp/                     # une séance par dossier
```

## Prérequis

- Docker Desktop récent (Windows, macOS ou Linux). Processeur x86 de préférence : sur ARM, le cluster Hadoop tourne en émulation (lent, voir « Images utilisées »).
- 8 Go de RAM (on ne lance qu'un profil à la fois) et 15 Go de disque libre.
- Python 3.9 ou plus sur la machine, pour les scripts de vérification et de génération.
- Git.

Sous Windows, Docker Desktop tourne dans WSL2. Si le PC rame, limiter la mémoire de WSL2 dans `%UserProfile%\.wslconfig` :

```ini
[wsl2]
memory=6GB
```

puis `wsl --shutdown` et relancer Docker Desktop.

## Démarrage

```bash
python scripts/verifier_env.py                 # tout doit être OK ou ATTENTION
docker compose --profile socle up -d           # S2 : Jupyter sur http://localhost:8888
docker compose --profile hadoop up -d          # S3, S4 : HDFS sur :9870, YARN sur :8088
python scripts/verifier_env.py --cluster       # vérifier le cluster Hadoop
```

| Commande | Effet |
| --- | --- |
| `docker compose --profile hadoop stop` | arrête, les données HDFS sont conservées |
| `docker compose --profile hadoop start` | redémarre là où on s'était arrêté |
| `docker compose --profile hadoop down` | arrête **et efface** le cluster |
| `docker compose logs -f namenode` | journaux d'un service |
| `docker compose exec namenode bash` | terminal dans le NameNode (commandes `hdfs`, `mapred`) |

## Données

Voir [`data/README.md`](data/README.md). Le gros fichier du mois (`clickstream_aout.csv`, 1,5 Go) est sur la clé USB, ou se génère :

```bash
python scripts/generer_clickstream.py --taille 1.5G --sortie data/clickstream_aout.csv
```

## Dépannage

| Symptôme | Piste |
| --- | --- |
| `port is already allocated` | un autre programme utilise le port : le fermer, ou `docker ps` pour trouver le conteneur |
| DataNodes à 0 dans `dfsadmin -report` | attendre 30 s après le démarrage ; sinon `docker compose logs datanode` |
| Le job MapReduce reste en *ACCEPTED* | pas assez de mémoire pour YARN : arrêter Jupyter et fermer le navigateur |
| Le noyau Jupyter meurt en S2 | c'est voulu au checkpoint 2 ; sinon, vérifier la mémoire de Docker |
| `docker compose` inconnu | Docker trop ancien : mettre à jour Docker Desktop |

## Images utilisées

| Image | Rôle | Remarque |
| --- | --- | --- |
| `apache/hadoop:3.5.0` | NameNode, DataNodes, ResourceManager, NodeManager | image officielle Apache, Ubuntu 24.04, Java 17, **amd64 seulement** : sur un processeur ARM (Mac M1 ou plus récent, Windows ARM), Docker l'émule, ce qui est nettement plus lent |
| `quay.io/jupyter/pyspark-notebook` | Jupyter, pandas, PySpark | projet Jupyter Docker Stacks |
