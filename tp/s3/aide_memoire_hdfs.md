# Aide-mémoire HDFS

Toutes ces commandes se tapent dans le NameNode (`docker compose exec namenode bash`).
Elles ressemblent aux commandes Linux, précédées de `hdfs dfs`.

## Fichiers et dossiers

| Commande | Effet |
| --- | --- |
| `hdfs dfs -ls -h /chemin` | lister, tailles lisibles |
| `hdfs dfs -mkdir -p /a/b` | créer un dossier (et ses parents) |
| `hdfs dfs -put local /hdfs/` | copier un fichier local vers HDFS |
| `hdfs dfs -get /hdfs/fichier local` | copier de HDFS vers le disque local |
| `hdfs dfs -head /hdfs/fichier` | premier kilo-octet du fichier |
| `hdfs dfs -tail /hdfs/fichier` | dernier kilo-octet |
| `hdfs dfs -cat /hdfs/fichier` | tout le fichier (attention aux gros fichiers) |
| `hdfs dfs -du -h /chemin` | taille, puis place occupée réplication comprise |
| `hdfs dfs -rm -r -f /chemin` | supprimer (sans corbeille dans notre TP) |
| `hdfs dfs -setrep -w 2 /hdfs/fichier` | changer le facteur de réplication et attendre |
| `hdfs dfs -D dfs.blocksize=32m -put ...` | choisir la taille de bloc à l'écriture |

## Administration

| Commande | Effet |
| --- | --- |
| `hdfs dfsadmin -report` | état du cluster : capacité, DataNodes vivants et morts |
| `hdfs dfsadmin -printTopology` | racks et DataNodes |
| `hdfs fsck /chemin -files -blocks -locations` | blocs d'un fichier et DataNodes qui les portent |
| `hdfs fsck /` | santé globale : blocs manquants, sous-répliqués |

## Interfaces web

| Adresse | Service |
| --- | --- |
| <http://localhost:9870> | NameNode (HDFS) |
| <http://localhost:8088> | ResourceManager (YARN), utile en S4 |

## Réglages de notre cluster (fichier `hadoop/hadoop.env`)

| Propriété | Valeur | Valeur par défaut de Hadoop |
| --- | --- | --- |
| `dfs.replication` | 3 | 3 |
| `dfs.blocksize` | 128 Mo | 128 Mo |
| `dfs.heartbeat.interval` | 3 s | 3 s |
| `dfs.namenode.heartbeat.recheck-interval` | 15 s | 5 min |

Un DataNode est déclaré mort après 2 × `recheck-interval` + 10 × `heartbeat.interval` : environ 1 min dans notre TP, 10 min 30 avec les valeurs par défaut.
