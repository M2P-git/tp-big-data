# S4 : MapReduce et YARN, calculer là où sont les données

> **Salma :** « Quelles sont les 10 marques les plus achetées ce mois-ci ? »

Le jeu papier de S1 porte enfin son nom : **MapReduce**. On l'écrit en Python avec **Hadoop Streaming**, qui fait tourner n'importe quel programme lisant l'entrée standard et écrivant sur la sortie standard.

| Fichier | Rôle | À compléter ? |
| --- | --- | --- |
| `mapper_evenements.py` | émet `type<TAB>1` pour chaque événement | oui |
| `reducer_somme.py` | additionne les valeurs de chaque clé | oui |
| `mapper_marques.py` | émet `marque<TAB>1` pour chaque achat | oui |
| `mapper_mots.py` | émet `mot<TAB>1` pour chaque mot des avis | oui (défi) |
| `simuler_mapreduce.py` | rejoue un job phase par phase sur votre machine | non |
| `test_s4.py` | vérifie vos scripts sur l'échantillon | non |

Les transparents de la séance suivent les mêmes manipulations, numérotées en étapes : démarrage = étape 1, checkpoint 1 = étapes 2 et 3, checkpoint 2 = étapes 4 et 5, checkpoint 3 = étape 6, checkpoint 4 = étape 7.

Démarrer le cluster (arrêté en fin de S3) puis entrer dans le NameNode :

```bash
docker compose --profile hadoop start
docker compose exec namenode bash
cd /tp/s4
```

## Checkpoint 1 : écrire et tester en local (15 min)

Compléter `mapper_evenements.py` et `reducer_somme.py` (les `TODO`), puis :

```bash
cat /data/echantillon/clickstream_echantillon.csv | python3 mapper_evenements.py | head
cat /data/echantillon/clickstream_echantillon.csv | python3 mapper_evenements.py | sort | python3 reducer_somme.py
python3 test_s4.py
```

Ce tube `mapper | sort | reducer` est exactement ce que fait Hadoop, sur une seule machine.

## Checkpoint 2 : voir les phases et l'effet du combiner (15 min)

```bash
python3 simuler_mapreduce.py --entree /data/echantillon/clickstream_echantillon.csv \
    --mapper mapper_evenements.py --reducer reducer_somme.py --splits 4 --reducers 2 \
    --sortie /tmp/simulation --verbeux
python3 simuler_mapreduce.py --entree /data/echantillon/clickstream_echantillon.csv \
    --mapper mapper_evenements.py --reducer reducer_somme.py --splits 4 --reducers 2 \
    --combiner reducer_somme.py --sortie /tmp/simulation --verbeux
```

**Q1.** Combien d'octets traversent le réseau (shuffle) sans combiner, puis avec ? Pourquoi `reducer_somme.py` peut-il servir de combiner, alors qu'un reducer qui calcule une moyenne ne le pourrait pas ?

## Checkpoint 3 : lancer le job sur le cluster (15 min)

```bash
hdfs dfs -rm -r -f /qissaria/sorties/evenements
mapred streaming \
  -files /tp/s4/mapper_evenements.py,/tp/s4/reducer_somme.py \
  -mapper "python3 mapper_evenements.py" \
  -reducer "python3 reducer_somme.py" \
  -input /qissaria/clickstream \
  -output /qissaria/sorties/evenements
hdfs dfs -cat /qissaria/sorties/evenements/part-*
```

Pendant le calcul, suivre le job sur <http://localhost:8088>.

**Q2.** Dans les compteurs affichés à la fin : combien de tâches map (*Launched map tasks*) ? Comparez au nombre de blocs vu en S3 (si le total est plus grand, regardez *Killed map tasks* : ce sont des copies de secours). Combien étaient *data-local*, combien *rack-local* ? Comment l'expliquez-vous dans notre cluster ?

**Q3.** Relancez avec un combiner (`-combiner "python3 reducer_somme.py"`, et un autre dossier de sortie). Comparez *Reduce shuffle bytes*.

## Checkpoint 4 : répondre à Salma (15 min)

Compléter `mapper_marques.py`, vérifier avec `python3 test_s4.py`, puis :

```bash
hdfs dfs -rm -r -f /qissaria/sorties/marques
mapred streaming \
  -files /tp/s4/mapper_marques.py,/tp/s4/reducer_somme.py \
  -mapper "python3 mapper_marques.py" \
  -combiner "python3 reducer_somme.py" \
  -reducer "python3 reducer_somme.py" \
  -input /qissaria/clickstream \
  -output /qissaria/sorties/marques
hdfs dfs -cat /qissaria/sorties/marques/part-* | sort -t$'\t' -k2,2nr | head -10
```

**Q4.** Quelles sont les 10 marques ? Le dernier tri (`sort | head`) se fait hors de Hadoop : pourquoi est-ce acceptable ici, et quand ne le serait-ce plus ?

## Défi : le comptage de mots (l'exemple historique de MapReduce)

Compléter `mapper_mots.py`, puis lancer le comptage des mots des avis clients sur le cluster :

```bash
hdfs dfs -mkdir -p /qissaria/avis
hdfs dfs -put /data/echantillon/avis_clients.tsv /qissaria/avis/
```

Écrivez vous-même la commande `mapred streaming` (sur le modèle ci-dessus), avec 2 reducers : ajoutez `-D mapreduce.job.reduces=2` juste après `mapred streaming`. Combien de fichiers `part-*` obtenez-vous, et pourquoi ?

## Réponses

À rendre dans `reponses_s4.md`.

## Dossier d'équipe

Le traitement batch principal de votre cas, écrit en pseudo-MapReduce : que fait le map, quelle est la clé, que fait le reduce ?
