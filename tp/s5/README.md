# S5 : Spark et PySpark, en pratique

**Question de Salma :** « Le top des marques a pris presque deux minutes sur le cluster. Demain, je veux cinq analyses, avec des filtres différents. Faut-il écrire cinq jobs MapReduce ? »

Toute la séance se fait dans un seul notebook, [`spark_s5.ipynb`](spark_s5.ipynb), avec une seule session Spark : ne redémarrez pas le noyau entre deux parties.

## Avant la séance : l'image Spark

Les quatre machines Spark utilisent l'image `quay.io/jupyter/pyspark-notebook:2026-10-19` (environ 7 Go, la même que le cluster du projet EFM). Téléchargez-la chez vous, pas en classe :

```bash
git pull
docker compose --profile spark pull
```

## Mettre à jour le dépôt et démarrer Spark

Dans PowerShell (ou un terminal), à la racine du dépôt :

```bash
git pull                                              # le profil spark et ce dossier tp/s5
docker compose --profile socle --profile hadoop stop  # libère le port 8888 et la mémoire
docker compose --profile spark up -d                  # master, 2 workers, Jupyter (environ 1 min la 1re fois)
python scripts/verifier_env.py --spark
```

Si `git pull` refuse parce que vous avez modifié des fichiers du dépôt (vos réponses de S4, par exemple) : `git stash`, puis `git pull`, puis `git stash pop`.

Ce que vous devez voir :

```
[OK       ] master Spark spark://spark-master:7077
[OK       ] 2 worker(s) vivant(s), 4 cœurs
[OK       ] Jupyter (driver) : PySpark 4.2.0
[OK       ] data/echantillon/clickstream_petit.csv présent
[OK       ] data/clickstream_aout.csv présent
```

Ouvrez ensuite <http://localhost:8888>, puis `tp/s5/spark_s5.ipynb`.

| Adresse | Ce que vous y voyez |
|---|---|
| <http://localhost:8888> | Jupyter : le notebook, dont le noyau est le **driver** |
| <http://localhost:8080> | le master Spark : deux workers, puis votre application |
| <http://localhost:4040> | votre application, tant que la session est ouverte : Jobs, Stages, SQL, Executors |

## Les machines du profil spark

| Conteneur | Rôle |
|---|---|
| `spark-master` | attribue les cœurs et la mémoire aux applications ; ne voit jamais les données |
| `spark-worker` (× 2) | lance un **executor** de 2 cœurs pour votre application |
| `jupyter-spark` | le notebook : son noyau Python est le **driver**, qui découpe le travail en tâches |

Le dépôt est monté en `/home/jovyan/work` dans les quatre conteneurs : chaque executor lit lui-même `data/`. La connexion au master est donnée par `compose.yaml` (variable `PYSPARK_SUBMIT_ARGS`) : le code du notebook ne la contient pas.

## Les données

| Fichier | Lignes | Sert à |
|---|---|---|
| `data/echantillon/clickstream_petit.csv` | 18 | tout vérifier à la main : 9 vues, 3 paniers, 6 achats |
| `data/clickstream_aout.csv` | environ 11 millions | le même calcul que le job MapReduce de S4 (clé USB, ou `scripts/generer_clickstream.py`) |
| `data/echantillon/catalogue_petit.csv`, `catalogue_doublon.csv` | 3 et 4 | les jointures, et le piège de la clé dupliquée |
| `data/echantillon/rayons.csv` | 10 | le rapport par rayon (petite table diffusée) |

Les résultats écrits par Spark (Parquet) vont dans `sorties/`, monté en écriture dans les quatre conteneurs. Sous Linux, si l'écriture est refusée : `chmod a+w sorties`.

Avec le cluster HDFS de S3 en marche (`docker compose --profile hadoop up -d`), le notebook peut aussi lire `hdfs://namenode:8020/qissaria/clickstream/clickstream_aout.csv`. Les comptes sont les mêmes.

## Ce que vous devez obtenir

| Étape | Résultat |
|---|---|
| Lecture du petit journal | 9 colonnes `string`, 18 lignes, une marque `NULL` |
| RDD et DataFrame | `cart` 3, `purchase` 6, `view` 9 dans les deux cas |
| Compteur de jobs | 1, 1, 1, 1, 2, 3 |
| Plan | `FileScan csv [event_type,brand]`, `partial_count`, `Exchange hashpartitioning(brand, 4)`, `count` |
| Mois d'août | 12 partitions ; view 10 280 795, cart 514 288, purchase 178 620 ; novatek 10 080 achats, comme en S4 |
| SQL | les mêmes comptes qu'en DataFrame ; `exceptAll` : `0 0` |
| Jointures | interne 17, gauche 18 ; avec le catalogue en double : 25 |
| Parquet | 30 dossiers `jour=...`, environ 125 Mo contre 1 500 Mo ; le 15 août : 376 544 événements |

## Fin de séance

Dernière cellule du notebook : `spark.stop()`. Puis :

```bash
docker compose --profile spark stop      # arrête Spark ; rien n'est effacé
```

## Dépannage

| Symptôme | Piste |
|---|---|
| `port is already allocated` sur 8888 | le Jupyter de S2 tourne encore : `docker compose --profile socle stop` |
| La cellule de la session ne rend pas la main | une autre application garde les 4 cœurs : `spark.stop()` dans l'autre notebook, ou redémarrer son noyau |
| `Path does not exist: file:/home/jovyan/work/data/clickstream_aout.csv` | le gros fichier n'est pas dans `data/` : clé USB, ou `python scripts/generer_clickstream.py --taille 1.5G --sortie data/clickstream_aout.csv` |
| Un executor meurt (*ExecutorLostFailure*) | pas assez de mémoire pour Docker : fermer le navigateur, arrêter le profil hadoop |
