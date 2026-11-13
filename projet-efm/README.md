# Projet de fin de module : Big Data et NoSQL

Dix sujets de projet, un par équipe, à réaliser et à soutenir en fin de module. Chaque sujet tourne sur un vrai cluster : HDFS, Spark avec deux workers, et une base NoSQL sur plusieurs nœuds. Les deux sujets en flux ajoutent Kafka. Un projet sans ces technologies n'est pas évalué.

## Par où commencer

1. Parcourez la présentation [projets-efm.pdf](projets-efm.pdf) et choisissez un sujet en équipe.
2. Lisez dans [fiches-projets.md](fiches-projets.md) la règle commune, les notions Big Data, puis la fiche de votre sujet en entier.
3. Dès la première semaine, installez et lancez le cluster en suivant son [mode d'emploi](cluster/README.md).

| Fichier | À quoi il sert |
| --- | --- |
| [projets-efm.pdf](projets-efm.pdf) | La présentation des sujets : règles, notions Big Data, cluster, puis les dix sujets |
| [fiches-projets.md](fiches-projets.md) | Les fiches détaillées : notions expliquées, puis pour chaque sujet son but, ses données, ses exigences et son évaluation |
| [cluster/](cluster/README.md) | Le cluster sur lequel tourne votre projet, son mode d'emploi et six exemples |

## Les sujets

Classés par famille technique et par difficulté croissante. Tous tournent en plus sur HDFS et sur le cluster Spark.

| N° | Sujet | Technologies imposées | Niveau |
| --- | --- | --- | --- |
| 01 | [E-commerce : ventes et segmentation client](fiches-projets.md#sujet-01) | Spark, Parquet, MongoDB | Accessible |
| 02 | [Qualité de l'air : fiabiliser un historique](fiches-projets.md#sujet-02) | Spark, Parquet, Cassandra | Accessible |
| 03 | [Technologies : cartographier les associations](fiches-projets.md#sujet-03) | Spark, Parquet, Neo4j | Accessible |
| 04 | [Taxis : prévoir la demande par zone](fiches-projets.md#sujet-04) | Spark MLlib, Parquet, MongoDB | Intermédiaire |
| 05 | [Avis clients : classer les retours écrits](fiches-projets.md#sujet-05) | Spark MLlib, Parquet, MongoDB | Intermédiaire |
| 06 | [Films : un service de recommandation](fiches-projets.md#sujet-06) | Spark ALS, Parquet, Redis | Avancé |
| 07 | [Transactions : repérer des réseaux suspects](fiches-projets.md#sujet-07) | Spark, Parquet, Neo4j | Intermédiaire |
| 08 | [Articles scientifiques : un moteur de recherche](fiches-projets.md#sujet-08) | Spark, Parquet, MongoDB | Intermédiaire |
| 09 | [Énergie : surveiller une consommation en continu](fiches-projets.md#sujet-09) | Kafka, Spark Streaming, Cassandra | Avancé |
| 10 | [Qissaria : compter les événements web en direct](fiches-projets.md#sujet-10) | Kafka, Spark Streaming, Redis | Avancé |

Sujets 01 à 03 : analyse par lots. 04 à 06 : apprentissage sur Spark. 07 et 08 : graphes et recherche. 09 et 10 : flux en temps réel.

## Cadre

- Équipes de 2 ou 3, deux équipes au plus par sujet, 3 à 4 semaines, 25 à 35 heures par personne.
- Le socle de chaque sujet permet d'obtenir 20 ; les extensions sont facultatives.
- Tout tourne sur CPU, sans API payante. Avec 16 Go de RAM, tous les sujets passent. Avec 8 Go, c'est serré, et les sujets 02 et 09 demandent au moins un PC de 16 Go dans l'équipe.
- Toutes les sources de données se téléchargent gratuitement, sans compte. Amazon Reviews 2023 n'affiche aucune licence : ne republiez pas le corpus. MovieLens est réservé à un usage de recherche : ne redistribuez pas l'archive.
