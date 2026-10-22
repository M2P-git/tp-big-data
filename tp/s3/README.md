# S3 : HDFS, stocker sur plusieurs machines

> **Salma :** « Si un disque tombe, perd-on tout l'historique ? »

Le cluster du TP : 1 NameNode, 4 DataNodes, 1 ResourceManager et 1 NodeManager, chacun dans son conteneur. Facteur de réplication : 3. Blocs : 128 Mo.

Aide-mémoire des commandes : [`aide_memoire_hdfs.md`](aide_memoire_hdfs.md). Répondez aux questions dans [`reponses_s3.md`](reponses_s3.md).

Les transparents de la séance suivent les mêmes manipulations, numérotées en étapes : checkpoint 1 = étapes 1 et 2, checkpoint 2 = étape 3, checkpoint 3 = étape 4, `-printTopology` (défi) = étape 5, checkpoint 4 = étape 6.

## Checkpoint 1 : démarrer le cluster (15 min)

Depuis la racine du dépôt, sur votre machine :

```bash
docker compose --profile socle stop          # libérer la mémoire de Jupyter
docker compose --profile hadoop up -d
docker compose ps                            # 7 conteneurs "running"
python scripts/verifier_env.py --cluster     # 4 DataNodes vivants
```

Interface web du NameNode : <http://localhost:9870> (onglet *Datanodes*).

Ouvrir un terminal **dans** le NameNode (toutes les commandes `hdfs` suivantes s'y tapent) :

```bash
docker compose exec namenode bash
hdfs dfsadmin -report
```

**Q1.** Combien de DataNodes sont vivants ? Quelle capacité totale annonce HDFS ? Pourquoi ce chiffre est-il trompeur dans notre TP ? (indice : où sont physiquement les 4 disques ?)

## Checkpoint 2 : charger le clickstream (15 min)

```bash
hdfs dfs -mkdir -p /qissaria/clickstream
hdfs dfs -put /data/clickstream_aout.csv /qissaria/clickstream/
hdfs dfs -ls -h /qissaria/clickstream
hdfs dfs -du -h /qissaria
hdfs dfs -head /qissaria/clickstream/clickstream_aout.csv
```

**Q2.** `-du` affiche deux tailles. Que représente la seconde ? Vérifiez le rapport entre les deux.

## Checkpoint 3 : voir les blocs et leurs copies (15 min)

**Prédiction d'abord :** combien de blocs pour un fichier de 1,5 Go ? Combien de copies de blocs en tout ?

```bash
hdfs fsck /qissaria/clickstream/clickstream_aout.csv -files -blocks -locations
```

Même chose dans l'interface web : *Utilities*, *Browse the file system*, cliquer sur le fichier, menu *Block information*.

Recharger le fichier avec des blocs de 32 Mo :

```bash
hdfs dfs -mkdir -p /qissaria/petits_blocs
hdfs dfs -D dfs.blocksize=32m -put /data/clickstream_aout.csv /qissaria/petits_blocs/
hdfs fsck /qissaria/petits_blocs -files -blocks | tail -20
```

**Q3.** Combien de blocs maintenant ? Pourquoi HDFS préfère-t-il de gros blocs ? (pensez au NameNode, qui garde en mémoire la liste de tous les blocs)

## Checkpoint 4 : provoquer une panne (15 min)

Sur votre machine (pas dans le NameNode), arrêter un DataNode :

```bash
docker ps --filter name=datanode --format "{{.Names}}"
docker stop bigdata-nosql-datanode-2
```

Dans le NameNode, observer pendant 2 à 3 minutes :

```bash
hdfs dfsadmin -report | grep -E "Live|Dead"
hdfs fsck /qissaria | grep -iE "under-replicated|status"
hdfs dfs -head /qissaria/clickstream/clickstream_aout.csv   # le fichier reste lisible ?
```

Puis redémarrer le DataNode et observer de nouveau :

```bash
docker start bigdata-nosql-datanode-2
```

**Q4.** Racontez la séquence : que détecte le NameNode, au bout de combien de temps, et que fait-il ? Qu'a-t-on perdu pendant la panne ?

**Q5.** Que se passe-t-il quand le DataNode revient ? Pourquoi certains blocs ont-ils alors 4 copies pendant un moment ?

## Défis (pour ceux qui ont fini)

- `hdfs dfs -setrep -w 2 /qissaria/petits_blocs/clickstream_aout.csv` : que change `-w` ?
- `hdfs dfsadmin -printTopology` : dans quel rack sont nos DataNodes ? Que perdrait-on en vrai si les 3 copies d'un bloc étaient dans le même rack ?

## Fin de séance

```bash
exit                                        # sortir du NameNode
docker compose --profile hadoop stop        # arrête sans effacer (on reprend en S4)
```

Attention : `docker compose --profile hadoop down` **efface** le cluster et tout ce qu'il contient.

## Dossier d'équipe

Plan de stockage de votre cas : volume brut, réplication, nombre de DataNodes.
