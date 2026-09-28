# S2 : Une machine ne suffit plus

> **Salma :** « Le rapport mensuel du trafic fait planter le serveur. Pourquoi ? »

## Avant le TP : installation (en classe)

1. Installer Docker Desktop (ou le charger depuis la clé USB) et le démarrer.
2. Cloner le dépôt, puis vérifier le poste depuis sa racine :

   ```bash
   git clone <adresse du dépôt> bigdata-nosql-tp
   cd bigdata-nosql-tp
   python scripts/verifier_env.py
   ```

3. Charger les images depuis la clé USB (plus rapide que le Wi-Fi) :

   ```bash
   docker load -i E:/images/jupyter-pyspark.tar
   docker load -i E:/images/hadoop-3.5.0.tar
   ```

4. Copier `clickstream_aout.csv` de la clé dans le dossier `data/`.

## Le TP

```bash
docker compose --profile socle up -d
```

Ouvrir <http://localhost:8888>, puis `tp/s2/limite_memoire.ipynb`, et suivre les quatre checkpoints.

Le conteneur Jupyter est volontairement limité à 2 Go de mémoire (voir `compose.yaml`) : c'est notre « petit serveur ».

À la fin de la séance :

```bash
docker compose --profile socle stop
```

## Dossier d'équipe

Premier schéma de la pile cible de votre cas : collecte, stockage, traitement, analyse, restitution.
