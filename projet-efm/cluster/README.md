# Le cluster du projet

Ce dossier contient le cluster sur lequel tourne votre projet. Chaque couche y fonctionne sur plusieurs nœuds, comme en production, mais sur votre seule machine grâce à Docker. Chaque nœud est un processus séparé, avec sa mémoire, son disque et son adresse réseau : c'est un vrai système distribué, comme le cluster Hadoop des TP de S3 et S4.

| Couche | Nœuds | Ce qui est réparti |
| --- | --- | --- |
| HDFS | 1 NameNode, 3 DataNodes | les fichiers, en blocs de 16 Mo, chaque bloc en 2 copies |
| Spark | 1 master, 2 workers de 2 cœurs, Jupyter comme driver | les tâches de calcul |
| MongoDB | 2 shards, 1 serveur de configuration, 1 routeur | les documents, selon la clé de sharding |
| Cassandra | 2 nœuds, un 3e en option | les partitions, en 2 copies |
| Redis | 3 nœuds principaux, 3 répliques | les clés, selon leur hachage |
| Kafka | 3 brokers | les partitions des topics, en 2 copies |
| Neo4j | 1 instance | rien : le cluster Neo4j est réservé à l'édition payante |

Il vous faut Docker Desktop, comme pour les TP. Arrêtez l'environnement des TP avant de lancer le cluster : les deux utilisent le port 8888 de Jupyter.

## 1. La machine qu'il faut

Vous ne lancez que les couches de votre sujet. La mémoire indiquée est celle qu'il faut donner à Docker : c'est le pic atteint pendant un traitement, tous les conteneurs de la pile réunis.

| Sujets | Profils à lancer | Mémoire à donner à Docker |
| --- | --- | --- |
| 01, 04, 05, 08 | `hdfs` `spark` `mongo` | 5,3 Go |
| 02 | `hdfs` `spark` `cassandra` | 6 Go |
| 03, 07 | `hdfs` `spark` `neo4j` | 5,5 Go |
| 06 | `hdfs` `spark` `redis` | 4,8 Go |
| 09 | `hdfs` `spark` `kafka` `cassandra` | 8 Go environ |
| 10 | `hdfs` `spark` `kafka` `redis` | 5,4 Go |

- **16 Go de RAM : tous les sujets passent.** Par défaut, Docker Desktop reçoit la moitié de la RAM, soit 8 Go.
- **8 Go de RAM : c'est juste.** Donnez 6 Go à Docker (voir ci-dessous), fermez le navigateur pendant les traitements, et ne lancez qu'un worker Spark si la mémoire manque. Les sujets 02 et 09 ne passent pas : il faut au moins un PC de 16 Go dans l'équipe.
- **Disque : 25 Go libres.** Les images pèsent environ 11 Go par sujet une fois décompressées, dont 7 Go pour l'image Spark.
- **Processeur x86 de préférence.** L'image Hadoop n'existe qu'en x86 : sur un PC ARM, HDFS tourne en émulation, donc plus lentement.

Sous Windows, la mémoire de Docker se règle dans `%UserProfile%\.wslconfig`, puis `wsl --shutdown` et relance de Docker Desktop :

```ini
[wsl2]
memory=6GB
```

## 2. Démarrer

Depuis ce dossier :

```bash
docker compose --profile spark build                          # une fois, environ 1 minute
docker compose --profile hdfs --profile spark --profile mongo up -d
```

Remplacez `mongo` par les profils de votre sujet. Pour `build`, n'ajoutez pas l'option `-q` : Docker peut alors refuser silencieusement la construction.

| Interface | Adresse |
| --- | --- |
| Jupyter | http://localhost:8888 |
| Spark : master et workers | http://localhost:8080 |
| Spark : votre application en cours | http://localhost:4040 |
| HDFS | http://localhost:9870 |
| Neo4j | http://localhost:7474, utilisateur `neo4j`, mot de passe `projet-efm` |

Cassandra met environ 2 min 30 s à démarrer ses deux nœuds, l'un après l'autre. Les autres couches sont prêtes en moins d'une minute.

## 3. Charger les données dans HDFS

Déposez vos fichiers bruts dans le dossier `donnees/`, puis copiez-les dans HDFS :

```bash
docker compose exec namenode hdfs dfs -mkdir -p /brut
docker compose exec namenode hdfs dfs -put -f /donnees/ventes.csv /brut/
docker compose exec namenode hdfs fsck /brut/ventes.csv -files -blocks -locations
```

La dernière commande montre chaque bloc et les deux DataNodes qui en gardent une copie. Un fichier de 136 Mo donne 9 blocs.

**Sous Git Bash**, tapez `export MSYS_NO_PATHCONV=1` avant ces commandes. Sinon, Git Bash transforme `/brut` en chemin Windows et HDFS répond `No FileSystem for scheme "C"`. PowerShell n'a pas ce problème.

## 4. Lancer un traitement

Dans un notebook Jupyter, une session Spark se connecte d'elle-même au cluster et lit HDFS par défaut :

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("mon-projet").getOrCreate()
df = spark.read.csv("/brut/ventes.csv", header=True)      # lu dans HDFS
df.write.mode("overwrite").partitionBy("mois").parquet("/propre/ventes")
```

Pour un script, depuis un terminal Jupyter ou depuis votre machine :

```bash
docker compose exec jupyter spark-submit /home/jovyan/work/mon_script.py
```

Votre dossier `travail/` est monté dans Jupyter sous `/home/jovyan/work`.

**Une application à la fois.** Une session Spark prend tous les cœurs des workers. Si un notebook garde sa session ouverte, un `spark-submit` lancé à côté attend des cœurs libres sans rien dire. Fermez la session du notebook avec `spark.stop()`, ou limitez chaque application avec `.config("spark.cores.max", "2")`.

Les bibliothèques Python des bases sont installées dans Jupyter et dans les workers : `pymongo`, `cassandra-driver`, `redis`, `neo4j`, `kafka-python`. Le connecteur Kafka de Spark est inclus dans l'image : votre démonstration ne dépend pas d'internet.

## 5. Les exemples fournis

Ils sont dans `exemples/`, visibles dans Jupyter sous `/home/jovyan/exemples`. Pour les essayer, générez un million d'événements Qissaria avec le script des TP, chargez-les dans HDFS, puis lancez le premier exemple. Depuis ce dossier :

```bash
python ../../scripts/generer_clickstream.py --lignes 1000000 --graine 42 --sortie donnees/clickstream.csv
docker compose exec namenode hdfs dfs -mkdir -p /brut
docker compose exec namenode hdfs dfs -put -f /donnees/clickstream.csv /brut/
docker compose exec jupyter spark-submit /home/jovyan/exemples/premier_job.py /brut/clickstream.csv
```

Avec la graine 42, vous devez obtenir les résultats de la dernière colonne.

| Exemple | Ce qu'il montre | Ce que vous devez obtenir |
| --- | --- | --- |
| `premier_job.py` | lecture HDFS, `groupBy` réparti, écriture Parquet partitionnée | 9 partitions, des tâches sur les 2 exécuteurs ; 937 244 vues, 46 557 paniers, 16 199 achats |
| `vers_mongo.py` | écriture rejouable dans MongoDB shardé depuis les workers | 81 708 documents, à peu près moitié sur chaque shard ; le même total à la relance |
| `vers_cassandra.py` | écriture rejouable dans Cassandra, clé de partition et clé de tri | 90 lignes, identiques à la relance |
| `vers_redis.py` | classements dans des ensembles ordonnés, répartis sur Redis Cluster | 30 clés réparties sur les 3 nœuds principaux, identiques à la relance |
| `producteur.py` | rejeu d'un CSV dans Kafka à débit réglable, avec identifiant et instant d'émission | jusqu'à 4 000 messages par seconde |
| `flux_compteurs.py` | fenêtres de 5 minutes, watermark, checkpoint dans HDFS, écriture rejouable dans Redis | après un arrêt brutal et une relance, chaque compteur égal au calcul par lots |

Ce sont des points de départ, pas des solutions : aucun ne traite les données de votre sujet.

## 6. Montrer la répartition

| Couche | Commande | Ce qu'on voit |
| --- | --- | --- |
| HDFS | `hdfs fsck <fichier> -files -blocks -locations` | les blocs et leurs copies |
| Spark | http://localhost:4040, onglet *Executors* | les tâches de chaque worker, le shuffle lu et écrit |
| MongoDB | `db.clients.getShardDistribution()` dans `mongosh --host mongo-router` | les documents de chaque shard |
| Cassandra | `nodetool status` et `nodetool getendpoints <keyspace> <table> <clé>` | les nœuds, et ceux qui portent une clé |
| Redis | `redis-cli -h redis1 cluster nodes` et `cluster keyslot <clé>` | les emplacements de hachage de chaque nœud |
| Kafka | `/opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka1:9092 --describe --topic <topic>` | le leader et les copies de chaque partition |

Chaque commande se lance avec `docker compose exec <service> ...`, par exemple `docker compose exec cassandra1 nodetool status`.

## 7. Provoquer une panne

Votre démonstration de soutenance doit en montrer une. Arrêtez un nœud avec `docker compose stop <service>`, ou tuez-le avec `docker compose kill <service>`. Voici ce qui se passe :

| Panne | Ce qui se passe |
| --- | --- |
| Un DataNode arrêté | la lecture réussit grâce à la seconde copie, mais ralentit nettement pendant environ une minute, le temps que le NameNode déclare le nœud mort |
| Un worker Spark tué en plein traitement | le traitement se termine avec le même résultat : l'autre exécuteur reprend les tâches perdues |
| Un shard MongoDB arrêté | les requêtes qui ont besoin de ce shard restent bloquées plusieurs dizaines de secondes, puis échouent : répartir sans répliquer ne protège pas des pannes |
| Un nœud Cassandra arrêté | une lecture en cohérence `ONE` répond ; en `QUORUM`, elle échoue, car 2 copies exigent les 2 nœuds |
| Un nœud principal Redis arrêté | sa réplique prend le relais : la clé redevient lisible en une dizaine de secondes |
| Le traitement en flux tué puis relancé | il repart de son checkpoint ; aucun événement n'est perdu ni compté deux fois |

Relancez ensuite le nœud avec `docker compose start <service>`.

Deux pièges à connaître. Un client Redis Cluster doit recevoir plusieurs nœuds d'entrée : s'il n'en connaît qu'un et que celui-ci tombe, il ne trouve plus le cluster. Et un producteur Kafka relancé renvoie ses messages en double : c'est l'identifiant de chaque message qui permet de les écarter.

## 8. Mesurer le passage à l'échelle

Lancez le même traitement avec un puis deux workers :

```bash
docker compose stop spark-worker2      # un seul worker
docker compose start spark-worker2     # de nouveau deux
```

Sur le million d'événements de l'exemple, `premier_job.py` prend à peu près le même temps avec un ou deux workers. Le second worker n'accélère rien : il partage les mêmes cœurs et le même disque, et sur un si petit volume, la coordination coûte plus qu'elle ne rapporte. C'est un résultat à expliquer dans votre rapport, pas à cacher. Pour voir un gain, il faut un volume plus gros, ou de vraies machines séparées.

## 9. Arrêter et effacer

```bash
docker compose --profile '*' stop       # tout s'arrête, rien n'est perdu
docker compose --profile '*' down       # efface les bases et les topics ; HDFS est gardé
docker compose --profile '*' down -v    # efface tout, HDFS compris
```

HDFS est votre lac de données : il survit à `down`. Les bases se reconstruisent depuis HDFS en relançant votre pipeline, qui doit donc être rejouable.

## 10. En bonus : un nœud par machine

Le même fichier peut servir à placer des nœuds sur les PC des membres de l'équipe, sur un réseau que vous maîtrisez : switch filaire ou partage de connexion d'un téléphone. Il faut alors publier les ports de chaque service et faire annoncer à chaque nœud l'adresse IP de sa machine. C'est la seule façon de mesurer ce qu'une machine unique ne montre pas : le coût réel du réseau. Gardez toujours une démonstration de secours sur une seule machine.
