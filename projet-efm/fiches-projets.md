# Projet de fin de module : les fiches des dix sujets

ISMAGI - CI3 AI - Année universitaire 2026-2027
Enseignant : Dr Paul Menounga Mbilong

Ce document complète la présentation `projets-efm.pdf`. La présentation sert à choisir un sujet ; les fiches servent à le réaliser.

Lisez dans cet ordre :

1. [La règle commune](#la-règle-commune--des-technologies-big-data-obligatoirement) et [ce que j'attends de tous les projets](#ce-que-jattends-de-tous-les-projets).
2. [Les notions Big Data du projet](#les-notions-big-data-du-projet) : ce que chaque notion veut dire, à quoi elle sert, comment la montrer.
3. La fiche de votre sujet en entier, en particulier son but et le tableau des notions qu'il travaille. Revenez-y à chaque jalon.

## La règle commune : des technologies Big Data, obligatoirement

Le projet est noté dans un module Big Data et NoSQL. **Un projet qui n'utilise pas ces technologies n'est pas évalué**, même s'il fonctionne et donne de bons résultats.

Pour les dix sujets, sans exception :

| Imposé | Ce que cela veut dire concrètement |
| --- | --- |
| **Spark (PySpark)** | Toute la préparation, le nettoyage et les agrégations se font en DataFrame Spark. Pandas est toléré pour tracer un graphique ou afficher un petit résultat, jamais pour traiter le jeu complet. Pas de `collect()` sur toutes les données suivi d'une boucle Python. |
| **Parquet** | Les données nettoyées sont écrites en Parquet, avec au moins un choix de partitionnement que vous expliquez. Montrez le plan d'exécution ou l'onglet Spark UI d'un traitement. |
| **Une base NoSQL** | MongoDB, Cassandra, Redis ou Neo4j selon le sujet. Elle sert des requêtes réelles depuis votre application : schéma, clés, index ou ordre de tri, et au moins une mesure avant / après. Une base remplie une fois et jamais interrogée ne compte pas. |
| **Kafka** | Pour les sujets 09 et 10 uniquement. |
| **HDFS et le cluster** | Les données brutes et les fichiers Parquet vivent dans HDFS. Spark tourne sur le cluster, jamais en mode local pour le rendu. La base NoSQL tourne sur plusieurs nœuds, sauf Neo4j. Le cluster est fourni avec son mode d'emploi : dossier [cluster](cluster/README.md). |

Le cluster tourne dans Docker, sur une seule machine : c'est un vrai système distribué, comme le cluster Hadoop des TP. Placer un nœud sur chaque PC de l'équipe est un bonus, jamais une obligation. Voir [Un vrai cluster, sur une seule machine](#notion-cluster).

Tout tourne sur CPU. Aucun GPU, aucune API d'IA payante. Selon le sujet, il faut donner 5 à 6 Go de mémoire à Docker, environ 8 Go pour le sujet 09. Avec 16 Go de RAM, tous les sujets passent. Avec 8 Go, c'est serré, et les sujets 02 et 09 demandent au moins un PC de 16 Go dans l'équipe. Le détail est dans le [README du cluster](cluster/README.md).

## Organisation

- Équipes de 2 ou 3. Un sujet par équipe, deux équipes au plus sur le même sujet. Le choix se fait à la prochaine séance.
- Comptez 25 à 35 heures de travail par personne, sur 3 à 4 semaines.
- Lancez le cluster dès le premier jalon. Au deuxième jalon, un extrait de vos données doit traverser tout le cluster.
- Chaque fiche donne deux volumes : un petit pour développer, puis le volume attendu pour le rendu. Commencez toujours par le petit. Monter en volume est un jalon, pas un point de départ.
- Les niveaux « accessible », « intermédiaire » et « avancé » indiquent la prise en main : combien de notions nouvelles il faut assembler. Ils ne plafonnent pas la note. Le socle de n'importe quel sujet permet d'avoir 20.
- La partie « si vous avez le temps » de chaque fiche est facultative. Elle n'apporte des points que si elle est faite et évaluée aussi sérieusement que le socle.

## Les dix sujets

| N° | Sujet | Technologies imposées | Niveau |
| --- | --- | --- | --- |
| **Analyse par lots** | | | |
| 01 | [E-commerce : ventes et segmentation client](#sujet-01) | Spark, Parquet, MongoDB | Accessible |
| 02 | [Qualité de l'air : fiabiliser un historique](#sujet-02) | Spark, Parquet, Cassandra | Accessible |
| 03 | [Technologies : cartographier les associations](#sujet-03) | Spark, Parquet, Neo4j | Accessible |
| **Apprentissage sur Spark** | | | |
| 04 | [Taxis : prévoir la demande par zone](#sujet-04) | Spark MLlib, Parquet, MongoDB | Intermédiaire |
| 05 | [Avis clients : classer les retours écrits](#sujet-05) | Spark MLlib, Parquet, MongoDB | Intermédiaire |
| 06 | [Films : un service de recommandation](#sujet-06) | Spark ALS, Parquet, Redis | Avancé |
| **Graphes et recherche** | | | |
| 07 | [Transactions : repérer des réseaux suspects](#sujet-07) | Spark, Parquet, Neo4j | Intermédiaire |
| 08 | [Articles scientifiques : un moteur de recherche](#sujet-08) | Spark, Parquet, MongoDB | Intermédiaire |
| **Flux en temps réel** | | | |
| 09 | [Énergie : surveiller une consommation en continu](#sujet-09) | Kafka, Spark Streaming, Cassandra | Avancé |
| 10 | [Qissaria : compter les événements web en direct](#sujet-10) | Kafka, Spark Streaming, Redis | Avancé |

Tous les sujets tournent en plus sur HDFS et sur le cluster Spark. Toutes les sources se téléchargent gratuitement, sans compte. Si un lien ne répond plus, prévenez-moi.

## Ce que j'attends de tous les projets

1. **Des données que l'on peut retrouver.** Un script ou une procédure de téléchargement, la source, la licence, la date, le périmètre retenu, la graine s'il y a échantillonnage. Pas de secrets ni de gros fichiers dans Git.
2. **Une qualité que l'on peut vérifier.** Un dictionnaire des colonnes avec types et unités, les règles de dédoublonnage et de rejet écrites noir sur blanc, les données brutes conservées telles quelles, les lignes rejetées conservées à part avec le motif.
3. **Un traitement Spark réparti que l'on peut expliquer.** Lancé sur le cluster, il lit et écrit dans HDFS. Les transformations, l'écriture Parquet, le partitionnement, et une observation du plan ou de l'exécution.
4. **Une base NoSQL qui sert à quelque chose.** Partez de trois requêtes que votre application doit servir, puis déduisez-en le schéma, les clés et les index. Dites pourquoi cette base plutôt qu'une autre du cours. Montrez comment la base répartit vos données entre ses nœuds.
5. **Une relance qui ne casse rien.** Rejouer un fichier ou un lot ne doit pas doubler les lignes ni les agrégats. Pour les sujets en flux : un arrêt, une reprise, et une politique claire pour les événements en retard.
6. **Des mesures comparables.** Même machine, même volume, même requête, au moins trois répétitions pour une durée ; médiane et état du cache précisés. Pour une latence p95, au moins 100 observations. Pour le passage à l'échelle, comparez un et deux workers Spark. Aucun seuil de performance n'est exigé : un résultat négatif bien mesuré et bien expliqué est recevable.
7. **Un modèle évalué, s'il y en a un.** Une référence naïve, un découpage entraînement / validation / test (dans le temps quand les données sont temporelles), des prétraitements appris sur l'entraînement seul, et une analyse des erreurs. Deux exemples qui marchent ne prouvent rien.
8. **Une restitution légère.** Une petite interface, un service interrogeable ou un parcours de démonstration scripté. Il ne s'agit pas de construire une application web complète.
9. **Une panne en direct.** Pendant la démonstration, vous arrêtez un nœud : un DataNode, un worker, un nœud de la base ou le traitement en flux. Vous montrez ce qui continue de marcher, ce qui casse, et pourquoi. Chaque fiche propose une panne.

## Les notions Big Data du projet

Cette partie explique les notions que les dix sujets mettent en œuvre. Chaque fiche de sujet indique ensuite lesquelles elle travaille et ce que vous en faites. Les notions sont présentées comme dans le cours : quoi, pourquoi, comment, et où vous les rencontrez.

<a id="notion-architecture"></a>

### Une même architecture pour tous les sujets

Tous les sujets suivent les couches d'une plateforme de données vues en S2. Seules changent la source des données et la base NoSQL.

| Étape | Son rôle | L'outil dans le projet |
| --- | --- | --- |
| Source | les données d'origine | fichier téléchargé, API, générateur |
| Collecte | les faire entrer dans la chaîne | script d'acquisition ; producteur Kafka pour les sujets 09 et 10 |
| Traitement | nettoyer, agréger, entraîner | Spark |
| Stockage | garder les données brutes et propres, prêtes à relire | HDFS, en Parquet partitionné |
| Service | répondre aux questions de l'application | MongoDB, Cassandra, Redis ou Neo4j |
| Restitution | montrer le résultat | petite interface ou démonstration scriptée |

**L'idée à retenir : Spark prépare, la base NoSQL sert.** Spark répond à la question « comment calculer sur toutes les données ? ». C'est un travail lourd, fait rarement, en parallèle. La base répond à « comment répondre vite à une question précise ? ». C'est un travail léger, fait souvent. On n'entraîne donc pas un modèle à chaque requête, et on ne parcourt pas toute la base à chaque clic.

<a id="notion-v"></a>

### Les cinq V, sujet par sujet

Le cours a présenté les V en S1 : chaque V appelle une réponse différente. Chaque sujet en touche plusieurs ; le tableau indique où chacun pose la difficulté principale.

| V | Ce qu'il vous demande | Où vous le rencontrez |
| --- | --- | --- |
| **Volume** | Répartir le calcul, lire le moins de données possible | 04 : près de 3 millions de trajets par mois ; 06 : une matrice de 10 milliards de cases ; 01 et 05 |
| **Vélocité** | Traiter les données au fil de l'eau, sans en perdre ni en compter deux fois | 09 et 10 : un flux continu, avec des retards et des doublons |
| **Variété** | Ramener des formes différentes à un modèle commun | 03 : des schémas qui changent chaque année ; 05 et 08 : du texte ; 07 : un graphe |
| **Véracité** | Contrôler, rejeter, signaler ce qui est douteux | 01 : annulations et retours ; 02 : capteurs en panne ; 03 : noms de technologies incohérents |
| **Valeur** | Prouver que le résultat sert à quelque chose | Tous : une référence naïve à battre, des mesures chiffrées |

Dans votre rapport, dites quel V vous a posé le plus de difficultés et ce que vous avez fait pour y répondre.

<a id="notion-cluster"></a>

### Un vrai cluster, sur une seule machine

Le Big Data, c'est répartir les données et les calculs sur plusieurs nœuds. Le projet le fait vraiment : chaque couche tourne sur plusieurs nœuds, comme en production. Ces nœuds sont des conteneurs Docker sur un même PC. Chacun est un processus séparé, avec sa mémoire, son disque et son adresse réseau, et ne parle aux autres que par le réseau. C'est une architecture sans partage (S2), comme le cluster Hadoop des TP de S3 et S4.

Un cluster sur une machine permet de voir et de manipuler :

- le découpage des fichiers en blocs et des données en partitions, réparties sur les nœuds ;
- la réplication et le placement des copies ;
- le shuffle entre les workers Spark ;
- la panne d'un nœud, la reprise des tâches, la bascule vers une réplique.

Il ne montre pas trois choses, parce que tous les nœuds partagent le même processeur, la même mémoire et le même disque :

- le vrai gain de vitesse : ajouter un worker n'ajoute pas de cœurs ;
- le coût réel du réseau ;
- des pannes matérielles indépendantes.

Ces trois points, vous les estimez par le calcul, comme en S1 et S2. Vous le constaterez avec l'exemple `premier_job.py` du cluster : sur 136 Mo, il prend à peu près le même temps avec un ou deux workers. Sur une seule machine et sur ce volume, le second worker n'apporte rien. C'est attendu, et c'est à expliquer.

| Couche | Nœuds | Ce que vous montrez |
| --- | --- | --- |
| HDFS | 1 NameNode, 3 DataNodes ; blocs de 16 Mo en 2 copies | où sont les blocs de vos fichiers |
| Spark | 1 master, 2 workers de 2 cœurs | les tâches réparties et le shuffle |
| MongoDB | 2 shards, 1 serveur de configuration, 1 routeur | la répartition des documents par la clé de sharding |
| Cassandra | 2 nœuds, réplication par 2 | les nœuds qui portent une partition |
| Redis | 3 nœuds principaux, 3 répliques | la répartition des clés par hachage |
| Kafka | 3 brokers | le leader et les copies de chaque partition |
| Neo4j | 1 instance | rien : le cluster Neo4j est réservé à l'édition payante. Un graphe se découpe d'ailleurs mal : chaque coupure casse des chemins |

Le mode d'emploi, les commandes et les pannes observées sont dans le [README du cluster](cluster/README.md). Six exemples y montrent comment lire HDFS, écrire dans chaque base depuis les workers et traiter un flux Kafka.

<a id="notion-spark"></a>

### Spark : un calcul réparti sur des partitions

- **Quoi ?** Un moteur de calcul qui découpe un DataFrame en **partitions** et traite chaque partition en parallèle, sur les cœurs de votre machine ou sur les nœuds d'un cluster.
- **Pourquoi ?** C'est l'héritier de MapReduce (S4), plus simple à écrire et plus rapide : les étapes s'enchaînent en mémoire au lieu d'écrire sur HDFS entre deux jobs.
- **Comment ?** Les **transformations** (`filter`, `select`, `groupBy`, `join`) ne calculent rien : elles construisent un plan. Une **action** (`count`, `write`, `show`) lance le calcul. Spark optimise d'abord le plan entier : il ne lit que les colonnes utiles et applique les filtres le plus tôt possible.
- **Où ?** Dans tous les sujets.

**Le lien avec MapReduce.** Un `groupBy` suivi d'une agrégation, c'est un map, un shuffle et un reduce. Les lignes de même clé traversent le réseau vers la même partition. Spark agrège d'abord sur place chaque partition, comme le combiner de S4, puis envoie les résultats partiels. Le shuffle reste l'étape chère. Un `join` entre deux grandes tables en provoque un aussi.

**Deux outils qui reviennent souvent.**

- `explode` transforme une cellule qui contient une liste en plusieurs lignes, une par élément (sujet 03).
- Les **fonctions de fenêtrage** (`Window` avec `lag`, `lead`, `rank`) calculent une valeur à partir des lignes voisines, par exemple l'heure précédente d'une même station (sujets 02 et 04). Ne les confondez pas avec les fenêtres de temps du streaming.

**Ce que vous montrez.** Le plan d'un traitement avec `explain()`, la durée de ses étapes dans Spark UI (par défaut à l'adresse `http://localhost:4040`), et l'absence de `collect()` sur toutes les données.

<a id="notion-parquet"></a>

### Parquet : stocker pour lire moins

- **Quoi ?** Un format de fichier rangé **par colonnes**, compressé, qui garde son schéma et des statistiques (minimum, maximum) pour chaque bloc de lignes.
- **Pourquoi ?** Avec un CSV, Spark lit toutes les lignes et toutes les colonnes, puis devine les types. Avec Parquet, il ne lit que les colonnes demandées et saute les blocs dont les statistiques montrent qu'ils ne contiennent rien d'utile pour le filtre.
- **Comment ?** `df.write.partitionBy("date").parquet(...)` crée un dossier par date. Un filtre sur la date ne lit que les dossiers utiles : c'est l'**élagage de partitions** (*partition pruning*). Le plan affiché par `explain()` le montre.
- **Où ?** Dans tous les sujets. Les sujets 01, 02 et 04 comparent en plus les deux formats, mesures à l'appui.

**Le piège.** Trop de partitions, c'est des milliers de petits fichiers, plus lents à ouvrir qu'un gros. Partitionnez sur une colonne souvent filtrée et qui a peu de valeurs distinctes : la date, la station, l'année. Jamais sur un identifiant de client.

<a id="notion-nosql"></a>

### Modéliser une base NoSQL : partir des requêtes

En relationnel, on modélise d'abord les données, puis on écrit les requêtes. En NoSQL, on fait l'inverse :

1. Écrivez en français les trois requêtes que votre application doit servir, avant d'écrire du code.
2. Pour chacune, choisissez la clé ou l'index qui mène droit aux données, sans parcourir toute la base.
3. Vérifiez par une mesure qu'aucune requête ne parcourt toute la base.

Deux idées surprennent souvent :

- **Dupliquer est normal.** La plupart des bases NoSQL ne font pas de jointures, ou les font mal. On range ensemble ce qu'on lit ensemble, quitte à copier une information à deux endroits.
- **La clé décide aussi de la répartition.** Sur un cluster, la clé de partition dit sur quel nœud vit chaque donnée. Une mauvaise clé crée un déséquilibre : un nœud surchargé pendant que les autres attendent, comme en MapReduce (S4).

| Base | Forme des données | Très bonne pour | Mauvaise pour | Comment le vérifier | Sujets |
| --- | --- | --- | --- | --- | --- |
| **MongoDB** | documents JSON dans des collections | requêtes variées, index secondaires, recherche texte | jointures entre collections | `explain("executionStats")` : `IXSCAN` plutôt que `COLLSCAN`, nombre de documents lus | 01, 04, 05, 08 |
| **Cassandra** | lignes rangées par clé de partition, triées par clé de regroupement | écritures massives, lecture d'une clé et d'une plage | toute requête sans la clé de partition | la requête passe sans `ALLOW FILTERING` ; `nodetool tablestats` donne la taille des partitions | 02, 09 |
| **Redis** | clé → valeur, en mémoire (chaînes, listes, ensembles ordonnés) | lectures très rapides, compteurs, classements, expiration | gros volumes, limités par la RAM ; requêtes complexes | `MEMORY USAGE` d'une clé ; latence mesurée côté client | 06, 10 |
| **Neo4j** | nœuds et relations, avec des propriétés | chemins, voisinages, motifs | agrégats sur toute la base | `PROFILE` devant une requête Cypher : nombre d'accès à la base | 03, 07 |

À la soutenance, on vous demandera pourquoi cette base et pas celle du sujet voisin. La réponse tient en une phrase sur vos requêtes.

<a id="notion-idempotence"></a>

### Relancer sans tout casser : l'idempotence

- **Quoi ?** Une écriture **idempotente** donne le même résultat qu'on la fasse une fois ou deux.
- **Pourquoi ?** La panne est la norme (S2). Spark relance des tâches qui ont échoué, Kafka peut relivrer un message, et vous relancerez votre pipeline des dizaines de fois pendant le projet. Une relance ne doit jamais doubler les données.
- **Comment ?** Donnez à chaque ligne une clé déterministe, calculée à partir des données et non tirée au hasard. Puis remplacez au lieu d'ajouter.
- **Où ?** Dans tous les sujets ; c'est le cœur des sujets 09 et 10.

| Ajoute : dangereux au rejeu | Remplace : rejouable |
| --- | --- |
| Parquet en mode `append` | Parquet en mode `overwrite`, partition par partition |
| MongoDB `insert` | MongoDB *upsert* sur une clé unique |
| Redis `INCR` | Redis `SET` de la valeur recalculée |

Avec Cassandra, un `INSERT` sur une clé primaire qui existe déjà remplace la ligne : l'écriture est idempotente si la clé l'est.

**Le test.** Lancez la chaîne deux fois, comptez les lignes, comparez les totaux. Ils doivent être identiques.

<a id="notion-mesures"></a>

### Mesurer pour argumenter

- **Durée d'un traitement.** Même machine, même volume, trois essais au moins ; on garde la médiane. Le premier essai est souvent plus lent : dites si le cache était froid ou chaud.
- **Latence d'une requête.** Le temps de réponse d'une requête. On donne la **p95** : 95 % des requêtes répondent plus vite que cette valeur. Il faut au moins 100 mesures, et dire d'où vous mesurez.
- **Débit.** Le nombre d'événements traités par seconde, une fois le flux stable.
- **Passage à l'échelle.** Comparez vos deux volumes. Volume et durée multipliés par 10 : le traitement passe à l'échelle. Volume multiplié par 10 et durée par 30 : un shuffle, un `collect()` ou une partition déséquilibrée vous freine. Trouvez lequel.

Le modèle d'une phrase de rapport : « Sur [volume], [traitement] prend [x] s sur CSV et [y] s sur Parquet, médiane de 3 essais, sur [machine]. Parquet lit [n] colonnes sur [m]. »

<a id="notion-mllib"></a>

### Apprendre à l'échelle avec Spark MLlib

- **Quoi ?** La bibliothèque d'apprentissage automatique de Spark. Le modèle s'entraîne sur un DataFrame réparti, sans le ramener sur une seule machine.
- **Pourquoi ?** Un entraînement repasse de nombreuses fois sur les données. C'est précisément ce que MapReduce faisait mal (S4) et que Spark fait bien, en gardant les données en mémoire.
- **Comment ?** Un `Pipeline` enchaîne les étapes : assemblage des variables (`VectorAssembler`), TF-IDF, modèle. On l'ajuste avec `fit()` sur l'entraînement, puis on l'applique avec `transform()` sur la validation et le test.
- **Où ?** Sujets 04, 05 et 06, et les extensions des sujets 01, 02 et 09.

Trois règles non négociables :

1. **Une référence naïve à battre** : la moyenne historique, la classe majoritaire, les films les plus populaires. Sans elle, un score ne veut rien dire.
2. **Un découpage dans le temps** quand les données sont datées : on entraîne sur le passé, on teste sur la suite. Jamais au hasard.
3. **Aucune fuite de données** : aucune information du futur ni du jeu de test ne doit servir à l'entraînement, même indirectement, par exemple en calculant le TF-IDF sur tout le corpus.

Un modèle se juge sur le test, face à la référence. Pas sur deux exemples qui marchent.

<a id="notion-kafka"></a>

### Kafka : un journal de messages

- **Quoi ?** Un journal distribué. Des **producteurs** y écrivent des messages, rangés dans un **topic** ; des **consommateurs** les lisent, chacun à son rythme.
- **Pourquoi ?** Il sépare celui qui produit de celui qui traite. Si Spark s'arrête, les messages attendent dans Kafka au lieu d'être perdus.
- **Comment ?** Un topic est découpé en **partitions**, réparties sur les nœuds. Dans une partition, chaque message a un numéro d'ordre : l'**offset**. Le consommateur retient l'offset où il en est, et peut revenir en arrière pour rejouer. L'ordre n'est garanti qu'à l'intérieur d'une partition ; deux messages de même clé vont dans la même partition.
- **Où ?** Sujets 09 et 10.

Dans vos sujets, il n'y a pas de vrais capteurs ni de vrai site : votre producteur lit un fichier historique et publie les lignes à un débit réglable. C'est un **rejeu**. Il ajoute à chaque message un identifiant stable et l'heure d'émission, pour mesurer le délai de bout en bout.

<a id="notion-streaming"></a>

### Spark Structured Streaming : fenêtres, retards, reprise

Structured Streaming traite un flux comme une table qui grandit sans cesse. Par défaut, il lit les nouveaux messages par **micro-lots**, à intervalle régulier. Quatre notions suffisent pour vos sujets :

- **Temps de l'événement.** On regroupe selon l'heure inscrite dans le message, quand la mesure ou le clic a eu lieu, et non selon l'heure d'arrivée chez Spark.
- **Fenêtre.** Un intervalle de temps, par exemple 5 minutes, sur lequel on agrège : `window(col("event_time"), "5 minutes")`. Une fenêtre reste ouverte tant que des événements peuvent encore y entrer.
- **Watermark.** Le retard maximal accepté, posé avec `withWatermark`. Elle dit : « j'attends les retardataires 10 minutes ; au-delà, je ferme la fenêtre et j'ignore ce qui arrive ». Sans watermark, Spark garde toutes les fenêtres en mémoire, indéfiniment.
- **Checkpoint.** Un dossier dans HDFS (`checkpointLocation`) où Spark note les offsets lus et l'état des fenêtres. Après un arrêt, il repart de là.

Pour écrire vers Cassandra ou Redis, on utilise souvent `foreachBatch` : Spark vous donne chaque micro-lot sous forme de DataFrame, avec son numéro.

**Compter chaque événement une fois et une seule.** Spark peut le garantir de bout en bout à deux conditions : une source que l'on peut rejouer, ce qu'est Kafka, et une écriture idempotente. La seconde condition, c'est à vous de la remplir.

---

<a id="sujet-01"></a>

## Sujet 01 - E-commerce : ventes et segmentation client

**Niveau : accessible.** **Technologies imposées :** HDFS, PySpark, Parquet, MongoDB shardé.

### Le problème

Une boutique en ligne veut savoir quels produits portent son chiffre d'affaires et quels groupes de clients elle sert. Ses données mélangent ventes, annulations et retours, et il faut les démêler avant de calculer quoi que ce soit.

### Le but du travail

Construire une chaîne par lots complète, du fichier brut jusqu'à une base qu'une application interroge. Le RFM n'est qu'un prétexte. Ce qui est évalué, c'est un traitement Spark juste, vérifié par des totaux qui se rapprochent, et des réponses MongoDB rapides grâce à des index bien choisis. C'est le sujet le plus direct pour comprendre la séparation entre préparation et service.

### Les notions Big Data travaillées

| Notion | Ce que vous en faites dans ce sujet | Explication |
| --- | --- | --- |
| Qualité des données | Écrire les règles de rejet, garder les lignes rejetées à part, rapprocher les totaux entre le brut et le nettoyé. | [Les cinq V](#notion-v) |
| Agrégation répartie | Le RFM est un `groupBy` par client : le shuffle rassemble sur une même partition toutes les lignes d'un client. | [Spark](#notion-spark) |
| Format colonnes | Parquet ne lit que les colonnes demandées. Vous le mesurez face au CSV, sur la même agrégation mensuelle. | [Parquet](#notion-parquet) |
| Index MongoDB | Sans index, MongoDB lit toute la collection ; avec, il va droit au document. `explain()` le montre. | [Modéliser une base NoSQL](#notion-nosql) |

### Les données

- **Source :** [UCI - Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii), licence CC BY 4.0 (citer Daqing Chen et UCI). Deux années de factures, environ 1,07 million de lignes, un classeur Excel à deux feuilles.
- **Accès :** téléchargez le classeur et convertissez chaque feuille une seule fois en CSV ou Parquet, en gardant les types d'origine. Le reste se fait sous Spark.
- **Volumes :** développement sur 20 000 lignes ; rendu sur les deux années, environ 1,07 million de lignes.
- **Attention :** les montants sont en livres sterling. Ne convertissez pas en dirhams sans le dire.

### Ce que vous devez livrer

1. Un contrôle des données : dates, clients manquants, prix nuls ou négatifs, quantités négatives, factures d'annulation.
2. Les ventes, les retours et le panier moyen, puis les indicateurs RFM (récence, fréquence, montant) par client.
3. Des segments de clients que vous savez expliquer avec des mots simples, et trois recommandations commerciales argumentées.

### Côté technique

Chaîne : classeur Excel → CSV → HDFS → Spark sur le cluster → Parquet dans HDFS → MongoDB shardé → petite interface.

**Le cluster.** Profils `hdfs`, `spark`, `mongo`. Choisissez la clé de sharding des profils clients et montrez comment les documents se répartissent entre les deux shards.

**Pourquoi MongoDB.** Un profil client est un document : récence, fréquence, montant, segment, date de calcul. Un document par (client, date de calcul), index unique sur ce couple. Vous devrez expliquer pourquoi pas Cassandra ici.

**Trois requêtes à servir :** la fiche d'un client ; tous les clients d'un segment ; les meilleurs produits d'un mois donné.

**Expérience à mener :** la même agrégation mensuelle lancée sur le CSV puis sur le Parquet : durée, octets lus, colonnes lues. Puis une requête MongoDB chronométrée avant et après création de l'index.

### Comment je l'évaluerai

- **Démonstration :** vous chargez un mois supplémentaire, vous relancez le pipeline, et vous m'expliquez pourquoi tel client a changé de segment.
- **Panne à montrer :** tuez un worker Spark pendant le calcul du RFM : le traitement doit se terminer avec les mêmes totaux.
- **Indicateurs :** taux de lignes rejetées et motifs ; rapprochement des montants entre brut et nettoyé ; durée du traitement Spark ; latence des requêtes avec et sans index.
- **Protocole :** fixez la date de référence du RFM. Comptez des factures distinctes pour la fréquence, pas des lignes. Traitez les retours à part. Vérifiez un petit lot à la main.
- **Pièges :** un client absent reste dans les ventes globales mais n'a pas de profil RFM. Deux lignes identiques ne sont pas forcément un doublon : justifiez votre règle.

### Si vous avez le temps

Comparer vos segments RFM à un K-means sur les mêmes variables normalisées, et interpréter les groupes obtenus.

---

<a id="sujet-02"></a>

## Sujet 02 - Qualité de l'air : fiabiliser un historique

**Niveau : accessible.** **Technologies imposées :** HDFS, PySpark, Parquet, Cassandra à deux nœuds.

### Le problème

Douze stations mesurent la pollution de Pékin heure par heure pendant quatre ans. Les capteurs tombent en panne, les séries ont des trous. On veut un historique propre, et surtout savoir quand il ne faut pas lui faire confiance.

### Le but du travail

Traiter la véracité à l'échelle. Il s'agit de repérer les trous et les doublons dans douze séries horaires de quatre ans, et de ne publier un chiffre que si les données le permettent. Puis de ranger ces séries pour qu'on puisse lire vite une période d'une station. Le sujet montre qu'une moyenne sans sa couverture peut tromper, et qu'un bon modèle Cassandra se déduit des lectures à servir.

### Les notions Big Data travaillées

| Notion | Ce que vous en faites dans ce sujet | Explication |
| --- | --- | --- |
| Qualité, en parallèle | Compter manquants, doublons et trous de chaque station en un seul passage Spark, sans boucle sur les stations. | [Spark](#notion-spark) |
| Fonctions de fenêtrage | `lag()` compare chaque heure à la précédente, station par station : un écart de plus d'une heure est une rupture. | [Spark](#notion-spark) |
| Élagage de partitions | Parquet partitionné par station et année : un filtre ne lit que les dossiers utiles. | [Parquet](#notion-parquet) |
| Clé de partition | Dans Cassandra, (station, année) décide où vivent les données ; le jour trie les lignes à l'intérieur de la partition. | [Modéliser une base NoSQL](#notion-nosql) |

### Les données

- **Source :** [UCI - Beijing Multi-Site Air Quality](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data), CC BY 4.0 (citer Song Chen et UCI). 420 768 observations horaires, 12 stations, polluants et météo, mars 2013 à février 2017. Un fichier CSV par station.
- **Accès :** téléchargez l'archive, harmonisez les douze fichiers, construisez un horodatage à partir des colonnes année, mois, jour, heure. Gardez les unités des polluants.
- **Volumes :** développement sur deux stations et un mois ; rendu sur les douze stations, quatre ans. Le jeu complet tient sur une machine.
- **Attention :** vos seuils servent à comparer des périodes entre elles. Ce ne sont pas des recommandations sanitaires.

### Ce que vous devez livrer

1. Un bilan par station : valeurs manquantes, doublons, ruptures dans la série temporelle.
2. Des agrégats journaliers accompagnés d'un taux de couverture : combien d'heures valides sur 24.
3. Un historique consultable et une table de caractéristiques prête pour un modèle.

### Côté technique

Chaîne : 12 CSV → HDFS → Spark sur le cluster → Parquet partitionné dans HDFS → Cassandra à deux nœuds → comparaison de stations.

**Le cluster.** Profils `hdfs`, `spark`, `cassandra`. Réplication par 2 : montrez avec `nodetool getendpoints` les nœuds qui portent une station.

**Pourquoi Cassandra.** Une série temporelle par station, lue par plage de dates : c'est son cas d'usage. Table journalière avec partition (station, année) et clé de tri sur le jour ; on y stocke les concentrations agrégées et le nombre d'heures valides. Vérifiez la taille de vos partitions.

**Requêtes à servir :** une période pour une station ; plusieurs stations sur la même période par lectures ciblées, sans `ALLOW FILTERING`.

**Expérience à mener :** un filtre sur une station et un mois, lu depuis le CSV brut puis depuis le Parquet avec sélection des colonnes et des partitions. Durée et octets lus.

### Comment je l'évaluerai

- **Démonstration :** une période à trous, sa couverture affichée, et ce que vaut la moyenne si on cache cette couverture.
- **Panne à montrer :** arrêtez un nœud Cassandra : une lecture en cohérence `ONE` répond, la même en `QUORUM` échoue. Expliquez pourquoi.
- **Indicateurs :** complétude par station ; nombre de jours publiables selon votre règle ; temps de lecture Parquet ; temps de requête Cassandra.
- **Protocole :** fixez avant l'analyse le nombre minimal d'heures valides pour publier une moyenne journalière. Gardez les valeurs brutes et un indicateur d'imputation à côté de toute valeur imputée.
- **Pièges :** remplacer une valeur manquante par zéro. Interpoler en utilisant le futur convient pour décrire un historique, mais fausse l'entraînement d'une prévision.

### Si vous avez le temps

Prévoir le PM2.5 de l'heure suivante et le comparer à la simple persistance (la valeur de l'heure précédente), avec MAE et découpage dans le temps, sans météo future.

---

<a id="sujet-03"></a>

## Sujet 03 - Technologies : cartographier les associations

**Niveau : accessible.** **Technologies imposées :** HDFS, PySpark, Parquet, Neo4j.

### Le problème

Chaque année, Stack Overflow interroge des dizaines de milliers de développeurs sur les outils qu'ils utilisent. Quelles technologies vont ensemble ? Qu'est-ce qui change d'une année à l'autre ? Le résultat doit aider quelqu'un à orienter son parcours d'apprentissage.

### Le but du travail

Gérer la variété. Trois enquêtes ont des schémas différents, et une seule cellule contient plusieurs réponses. Il faut les ramener à un modèle commun avec Spark, puis passer d'une table à un graphe que l'on peut parcourir. Le sujet fait toucher du doigt un piège classique du Big Data : une opération anodine, former des paires, peut multiplier le volume.

### Les notions Big Data travaillées

| Notion | Ce que vous en faites dans ce sujet | Explication |
| --- | --- | --- |
| Intégration de schémas | Une table de correspondance par année : les colonnes et les noms de technologies changent d'une édition à l'autre. | [Les cinq V](#notion-v) |
| Explosion combinatoire | `explode` change la cellule « Python;SQL;Java » en trois lignes. Qui cite 30 outils produit 435 paires : il faut borner. | [Spark](#notion-spark) |
| Déséquilibre des données | Quelques technologies très citées concentrent les paires. Spark UI montre des tâches bien plus longues que les autres. | [Spark](#notion-spark) |
| Parcours de graphe | Neo4j passe d'un nœud à ses voisins en suivant directement les relations, sans jointure. | [Modéliser une base NoSQL](#notion-nosql) |

### Les données

- **Source :** [Stack Overflow Developer Survey](https://survey.stackoverflow.co/), éditions 2024, 2025 et 2026, licence ODbL 1.0 pour la base et DbCL 1.0 pour les contenus. Archives officielles : [2024](https://github.com/StackExchange/Survey/tree/main/packages/archive/2024), [2025](https://github.com/StackExchange/Survey/tree/main/packages/archive/2025), [2026](https://github.com/StackExchange/Survey/tree/main/packages/archive/2026). Les CSV, de 117 à 152 Mo, sont stockés avec Git LFS : téléchargez-les avec le bouton de téléchargement brut de GitHub, sinon vous obtenez un fichier de quelques lignes.
- **Accès :** téléchargez pour chaque année le fichier de résultats et le schéma. Gardez les libellés bruts et construisez une table de correspondance des noms de technologies.
- **Volumes :** développement sur une année ; rendu sur les trois éditions 2024, 2025 et 2026, soit environ 400 Mo de CSV. Documentez les variables réellement comparables entre années plutôt que de tout charger.
- **Attention :** publiez des agrégats dans votre dépôt, pas de réponses individuelles.

### Ce que vous devez livrer

1. Les champs multi-valeurs éclatés et les noms de technologies harmonisés entre les années.
2. Les usages déclarés et les cooccurrences, avec les dénominateurs posés clairement.
3. Un graphe de technologies interrogeable par année.

### Côté technique

Chaîne : CSV des enquêtes → HDFS → Spark sur le cluster → Parquet harmonisé → Neo4j → exploration.

**Le cluster.** Profils `hdfs`, `spark`, `neo4j`. Neo4j reste sur une seule instance : la répartition porte sur HDFS et Spark, où l'explosion des paires fait le gros du travail. Expliquez pourquoi un graphe se découpe mal entre plusieurs machines.

**Pourquoi Neo4j.** « Qu'est-ce qui est utilisé avec Spark, et avec quoi ces outils sont-ils utilisés à leur tour ? » est un parcours de voisinage à plusieurs sauts. Nœud `Technologie` unique par nom canonique ; relation `UTILISE_AVEC` portant l'année, l'effectif et la proportion. On charge les associations agrégées, jamais les profils individuels.

**Requêtes à servir :** les voisins de Python ou de Spark ; la même association comparée entre deux années.

**Expérience à mener :** l'éclatement des champs multi-valeurs sous Spark, avec un nombre de paires par répondant borné ; le temps d'import dans Neo4j et la latence d'une requête de voisinage à deux sauts.

### Comment je l'évaluerai

- **Démonstration :** trois technologies suivies sur trois ans, et une association qui semble forte mais disparaît une fois les effectifs contrôlés.
- **Panne à montrer :** arrêtez un DataNode avant l'harmonisation : la lecture réussit grâce aux copies. Mesurez le ralentissement.
- **Indicateurs :** taux de correspondance entre schémas ; contrôles d'effectifs ; durée de transformation ; latence des requêtes.
- **Protocole :** déclarez les dénominateurs et un effectif minimal en dessous duquel vous n'affichez rien.
- **Pièges :** les répondants changent chaque année. « J'utilise » et « je veux apprendre » sont deux colonnes différentes. Une technologie populaire chez les répondants n'est pas forcément demandée par les recruteurs.

### Si vous avez le temps

Une mesure d'association corrigée de la popularité (par exemple un lift), et son classement comparé aux cooccurrences brutes.

---

<a id="sujet-04"></a>

## Sujet 04 - Taxis : prévoir la demande par zone

**Niveau : intermédiaire.** **Technologies imposées :** HDFS, PySpark, Spark MLlib, Parquet, MongoDB shardé.

### Le problème

Combien de taxis partiront de chaque zone de New York dans l'heure qui vient ? Une bonne estimation aide à placer les véhicules là où ils seront demandés.

### Le but du travail

Faire de l'apprentissage automatique sur des millions de lignes sans quitter Spark, en respectant le temps : on ne prévoit qu'avec ce que l'on savait au moment de prévoir. Puis servir les prévisions à une application. Le sujet réunit les trois briques du module : agrégation à grande échelle, apprentissage réparti et base de service.

### Les notions Big Data travaillées

| Notion | Ce que vous en faites dans ce sujet | Explication |
| --- | --- | --- |
| Volume et agrégation | Près de 3 millions de trajets en janvier 2024, ramenés à une grille d'environ 200 000 cases zone × heure. | [Spark](#notion-spark) |
| Jointures | La grille naît d'un `crossJoin` zones × heures, puis d'une jointure gauche avec les comptages : une heure vide vaut 0. | [Spark](#notion-spark) |
| Fonctions de fenêtrage | `lag()` donne, pour chaque zone, la demande de l'heure précédente, de la veille, de la semaine passée. | [Spark](#notion-spark) |
| Pipeline MLlib | Assemblage des variables puis régression, entraînés en parallèle. Découpage par date, jamais au hasard. | [MLlib](#notion-mllib) |

### Les données

- **Source :** [NYC TLC - Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), taxis jaunes : un fichier Parquet par mois, la table des zones et le dictionnaire des colonnes. Conservez l'attribution NYC TLC.
- **Accès :** téléchargez au moins trois mois de 2024, par exemple janvier à mars, et le dictionnaire de la même famille de taxis. Gardez un petit extrait de contrôle.
- **Volumes :** développement sur une semaine et quelques zones ; rendu sur trois mois au moins, près de 10 millions de trajets, en journées entières.
- **Attention :** les taxis jaunes ne décrivent pas tous les déplacements de la ville.

### Ce que vous devez livrer

1. Des trajets nettoyés et une grille zone × heure, y compris les heures sans aucun départ.
2. Des variables de calendrier et d'historique disponibles au moment où l'on fait la prévision.
3. Une référence naïve, une régression simple avec MLlib, et les prévisions servies dans MongoDB.

### Côté technique

Chaîne : Parquet TLC → HDFS → Spark et MLlib sur le cluster → MongoDB shardé → carte ou courbes.

**Le cluster.** Profils `hdfs`, `spark`, `mongo`. Choisissez la clé de sharding des prévisions, la zone hachée ou non, et justifiez-la par vos requêtes.

**Pourquoi MongoDB.** Un document par (zone, heure cible, version du modèle) qui réunit l'observé et le prévu, avec clé unique sur ce triplet. Index sur zone et heure pour lire un horizon de quelques heures.

**Requêtes à servir :** les prévisions des prochaines heures d'une zone, face aux départs réellement observés.

**Expérience à mener :** partitionnez le Parquet par date. Mesurez la lecture d'une journée contre la lecture complète, puis comparez un partitionnement raisonnable à un partitionnement trop fin.

### Comment je l'évaluerai

- **Démonstration :** vous prévoyez les derniers jours du mois, vous montrez une zone où le modèle bat la référence et une où il échoue.
- **Panne à montrer :** tuez un worker pendant l'entraînement : il doit se terminer, et vous comparez la MAE obtenue.
- **Indicateurs :** MAE globale et par zone, pour le modèle et pour la référence ; durée de préparation ; latence de consultation.
- **Protocole :** découpage entraînement / validation / test dans le temps, jamais au hasard. Pour chaque variable, notez l'instant où elle devient disponible.
- **Pièges :** la durée du trajet, le montant et le pourboire sont connus après coup : interdits comme variables. Un échantillon aléatoire de trajets fausse les comptages horaires ; échantillonnez des journées ou des zones entières.

### Si vous avez le temps

Un second mois, ou une météo historique alignée dans le temps, et le gain réel mesuré sur le même jeu de test.

---

<a id="sujet-05"></a>

## Sujet 05 - Avis clients : classer les retours écrits

**Niveau : intermédiaire.** **Technologies imposées :** HDFS, PySpark MLlib, Parquet, MongoDB shardé.

### Le problème

Un vendeur reçoit des milliers d'avis. Quels produits concentrent le mécontentement ? Peut-on repérer un avis négatif à partir du texte seul, et avec quelle marge d'erreur ?

### Le but du travail

Traiter du texte, une donnée non structurée, avec Spark. Il faut le transformer en vecteurs, entraîner un classifieur réparti, et mesurer honnêtement ce qu'il vaut face à une règle naïve. Le sujet apprend surtout à éviter la fuite de données, qui donne des scores flatteurs et faux.

### Les notions Big Data travaillées

| Notion | Ce que vous en faites dans ce sujet | Explication |
| --- | --- | --- |
| Variété : du texte | Lire du JSON compressé ligne à ligne, nettoyer, découper en mots : le texte devient des colonnes exploitables. | [Les cinq V](#notion-v) |
| TF-IDF réparti | Un mot pèse lourd s'il est fréquent dans l'avis et rare dans le corpus. Spark compte les mots sur toutes les partitions. | [MLlib](#notion-mllib) |
| Pipeline sans fuite | Découpage en mots, TF-IDF et modèle s'ajustent sur l'entraînement seul. Le test ne doit rien influencer. | [MLlib](#notion-mllib) |
| Cache | Les mêmes vecteurs servent à plusieurs entraînements : `cache()` évite de tout recalculer à chaque fois. | [Spark](#notion-spark) |

### Les données

- **Source :** [McAuley Lab - Amazon Reviews 2023](https://amazon-reviews-2023.github.io/), catégorie `All_Beauty` uniquement. Le téléchargement est gratuit et sans compte. La page n'affiche aucune licence, seulement un copyright : citez le laboratoire et la publication associée, et ne republiez pas le corpus.
- **Accès :** prenez le lien « review » de la catégorie sur la page officielle. Lisez le JSONL compressé en flux et gardez un échantillon reproductible avec ses identifiants.
- **Volumes :** développement sur 5 000 avis ; rendu sur 200 000 avis en anglais avec texte, note, produit et date ; la catégorie entière, environ 700 000 avis, si la mémoire le permet. Ne téléchargez pas les autres catégories.

### Ce que vous devez livrer

1. Un contrôle des textes vides et des doublons, la répartition des notes, puis les tendances par produit.
2. Un classificateur TF-IDF + régression logistique sous MLlib, comparé à la classe majoritaire.
3. Les avis, les prédictions et les erreurs du modèle consultables dans MongoDB.

### Côté technique

Chaîne : JSONL compressé → HDFS → Spark sur le cluster → TF-IDF + modèle → MongoDB shardé → exploration.

**Le cluster.** Profils `hdfs`, `spark`, `mongo`. Clé de sharding des avis : le produit ou l'avis ? La première regroupe les avis d'un produit sur un shard, la seconde équilibre mieux. Mesurez les deux.

**Pourquoi MongoDB.** Un avis est un document à texte libre, avec note, produit, date et version de prédiction. Index unique sur l'identifiant de l'avis ; index composé (produit, date).

**Requêtes à servir :** les avis négatifs récents d'un produit ; les cas où la note et la prédiction ne sont pas d'accord.

**Expérience à mener :** mettez en cache les caractéristiques réutilisées et chronométrez avec et sans. Puis mesurez les recherches par produit et date avec et sans l'index composé.

### Comment je l'évaluerai

- **Démonstration :** vous analysez un avis jamais vu, vous parcourez les erreurs du modèle et vous montrez des textes où la note représente mal le sentiment.
- **Panne à montrer :** arrêtez un shard MongoDB : montrez quelles requêtes échouent, et pourquoi répartir sans répliquer ne protège pas des pannes.
- **Indicateurs :** macro-F1 sur la cible issue des notes ; matrice de confusion ; gain par rapport à la classe majoritaire ; durée du traitement.
- **Protocole :** notes 1 et 2 → négatif, 4 et 5 → positif, 3 écarté du modèle binaire. Découpage dans le temps, dédoublonnage entre les jeux, TF-IDF ajusté sur l'entraînement seul.
- **Pièges :** la note est une cible approximative, pas la vérité sur le sentiment. L'identifiant de l'auteur n'a rien à faire dans les caractéristiques. Masquez la note quand vous annotez à la main.

### Si vous avez le temps

Annoter à l'aveugle 200 avis du jeu de test et comparer votre lecture à la cible issue des notes.

---

<a id="sujet-06"></a>

## Sujet 06 - Films : un service de recommandation

**Niveau : avancé.** **Technologies imposées :** HDFS, PySpark ALS, Parquet, Redis Cluster.

### Le problème

Recommander dix films à un utilisateur à partir de ce qu'il a noté. La vraie question : fait-on mieux que de lui proposer simplement les films les plus populaires ?

### Le but du travail

Séparer le calcul lourd de la réponse rapide. Spark entraîne ALS et calcule toutes les listes à l'avance ; Redis les rend en quelques millisecondes. Il faut aussi prouver que vos listes font mieux que les films populaires. C'est l'architecture de la plupart des systèmes de recommandation réels : un calcul par lots régulier, un service qui ne fait que lire.

### Les notions Big Data travaillées

| Notion | Ce que vous en faites dans ce sujet | Explication |
| --- | --- | --- |
| Matrice creuse | MovieLens 25M : environ 162 000 utilisateurs × 62 000 films, 10 milliards de cases dont 0,25 % sont remplies. | [Les cinq V](#notion-v) |
| Factorisation (ALS) | ALS résume chaque utilisateur et chaque film par quelques nombres, en calculant tour à tour les uns puis les autres, par blocs répartis. | [MLlib](#notion-mllib) |
| Précalcul et service | `recommendForAllUsers` produit les listes une fois ; à la requête, le service ne fait qu'une lecture de clé. | [Architecture](#notion-architecture) |
| Mémoire Redis | Tout est en RAM : estimez la taille de vos listes avant de les charger, et choisissez la structure (liste, ensemble ordonné). | [Modéliser une base NoSQL](#notion-nosql) |

### Les données

- **Source :** [GroupLens - MovieLens 25M](https://grouplens.org/datasets/movielens/25m/) et son [README](https://files.grouplens.org/datasets/movielens/ml-25m-README.html). Usage de recherche, attribution obligatoire, pas de redistribution de l'archive. Publiez votre script de téléchargement et vos résultats, pas les données.
- **Accès :** seuls `ratings.csv` et `movies.csv` servent au socle.
- **Volumes :** développement sur environ 100 000 notes ; rendu sur 1 à 5 millions de notes : tirez des utilisateurs avec une graine fixe et gardez toutes leurs notes. Les 25 millions sont facultatifs.

### Ce que vous devez livrer

1. Les interactions préparées et une recommandation de référence par popularité.
2. Un modèle ALS avec un petit nombre de facteurs, et dix recommandations par utilisateur.
3. L'exclusion des films déjà vus et un repli pour les utilisateurs inconnus.

### Côté technique

Chaîne : MovieLens → HDFS → Spark ALS sur le cluster → Redis Cluster → service top 10.

**Le cluster.** Profils `hdfs`, `spark`, `redis`. Montrez comment les clés des utilisateurs se répartissent sur les trois nœuds principaux de Redis.

**Pourquoi Redis.** Le service doit répondre en quelques millisecondes : on lit une liste précalculée, on n'entraîne rien à la requête. Une clé par (version du modèle, utilisateur), valeur = liste ordonnée de films et de scores. L'historique et le modèle sont persistés ailleurs ; Redis ne contient que ce qui doit être lu vite.

**Requêtes à servir :** le top 10 d'un utilisateur ; la liste populaire quand l'utilisateur est inconnu.

**Expérience à mener :** temps d'entraînement, mémoire consommée, latence de lecture Redis (p95 sur au moins 100 lectures). Évitez le calcul de tous les couples utilisateur-film.

### Comment je l'évaluerai

- **Démonstration :** deux profils comparés, aucun film déjà vu dans les listes, un identifiant inconnu qui déclenche le repli.
- **Panne à montrer :** arrêtez le nœud Redis qui porte un utilisateur : sa réplique prend le relais en une dizaine de secondes. Mesurez la latence pendant la bascule.
- **Indicateurs :** Recall@10 d'ALS contre la popularité ; couverture du catalogue ; part d'utilisateurs sans prédiction ; latence p95.
- **Protocole :** découpage des interactions dans le temps. Définissez ce qu'est un film « pertinent » (par exemple note ≥ 4) et publiez le nombre d'utilisateurs évaluables.
- **Pièges :** un bon RMSE sur les notes ne dit rien de la qualité d'un top 10. Ne faites pas disparaître en silence les utilisateurs ou films du test qui n'ont pas de prédiction : donnez leur proportion et montrez le repli.

### Si vous avez le temps

Un repli par genres pour les profils peu renseignés, et son apport mesuré sur ces profils.

---

<a id="sujet-07"></a>

## Sujet 07 - Transactions : repérer des réseaux suspects

**Niveau : intermédiaire.** **Technologies imposées :** HDFS, PySpark, Parquet, Neo4j.

### Le problème

Dans un réseau de virements, certains motifs intéressent un analyste : l'argent qui tourne en boucle entre quelques comptes, ou des dizaines de comptes qui alimentent le même. Il faut les trouver et expliquer pourquoi on les signale.

### Le but du travail

Comparer deux façons de suivre des liens dans les données : les jointures Spark et le parcours de graphe Neo4j. Il faut comprendre à partir de quand le graphe devient le bon outil, et produire des alertes qu'un humain peut vérifier en suivant un chemin.

### Les notions Big Data travaillées

| Notion | Ce que vous en faites dans ce sujet | Explication |
| --- | --- | --- |
| Données synthétiques | Un générateur à graine fixe redonne la même base à chaque lancement, avec une vérité terrain pour évaluer. | [Mesurer](#notion-mesures) |
| Agrégations Spark | Volumes entrants et sortants par compte : deux `groupBy` et une jointure, sur 50 000 transactions. | [Spark](#notion-spark) |
| Coût des sauts | En Spark, chaque saut d'un chemin est une jointure de plus, et le résultat grossit à chaque saut. | [Spark](#notion-spark) |
| Motifs Cypher bornés | Un motif de longueur variable trouve un circuit de 3 à 5 comptes. Sans borne, la recherche explose. | [Modéliser une base NoSQL](#notion-nosql) |

### Les données

- **Source :** vous les fabriquez. Aucune donnée bancaire réelle.
- **Accès :** un générateur à graine fixe produit des comptes, des transactions avec montant et horodatage, des scénarios normaux et des scénarios suspects (circuits, étoiles). La vérité terrain est écrite dans un fichier à part.
- **Volumes :** développement sur 500 comptes et 5 000 transactions ; rendu sur 10 000 comptes et 200 000 transactions ; test de charge facultatif à un million.
- **Attention :** écrivez partout, interface et rapport, que les données et les étiquettes sont simulées.

### Ce que vous devez livrer

1. Les transferts nettoyés et les volumes entrants et sortants par compte, calculés avec Spark.
2. Le graphe comptes / transactions dans Neo4j et trois règles de détection en Cypher.
3. Pour chaque alerte, le chemin qui l'explique et les transactions concernées.

### Côté technique

Chaîne : générateur → HDFS → Spark sur le cluster → Parquet → Neo4j → alertes expliquées.

**Le cluster.** Profils `hdfs`, `spark`, `neo4j`. Neo4j reste sur une seule instance : c'est côté Spark que chaque saut se paie en shuffle. Comptez les shuffles d'une recherche à trois sauts.

**Pourquoi Neo4j.** Chercher un cycle de longueur 3 à 5 en SQL, c'est une jointure par saut. En Cypher, c'est un motif. Nœuds `Compte` et `Transaction`, relations `EMET` (compte → transaction) et `VERS` (transaction → compte), identifiants uniques, montant et date sur la transaction.

**Requêtes à servir :** les circuits de longueur bornée sur une période ; les concentrations d'envois vers un même compte.

**Expérience à mener :** la même recherche de voisinage faite par jointures Spark et par parcours Neo4j, sur le même extrait, chronométrée. Bornez la longueur des parcours.

### Comment je l'évaluerai

- **Démonstration :** un circuit injecté suivi pas à pas jusqu'à l'alerte, puis un transfert normal signalé à tort et votre explication.
- **Panne à montrer :** tuez un worker pendant le calcul des volumes par compte : mêmes résultats attendus.
- **Indicateurs :** précision et rappel sur les scénarios injectés ; nombre de faux positifs ; temps d'import et de recherche.
- **Protocole :** les étiquettes servent à évaluer, jamais à détecter. Évaluez sur une graine différente de celle du développement, et incluez des motifs normaux qui ressemblent aux motifs suspects.
- **Pièges :** un cycle n'est pas une fraude. Vos scores valent pour votre générateur, pas pour une banque réelle.

### Si vous avez le temps

Des caractéristiques de graphe calculées sous Spark (degré, volumes, nombre de cycles) pour classer les alertes, comparées aux règles simples.

---

<a id="sujet-08"></a>

## Sujet 08 - Articles scientifiques : un moteur de recherche

**Niveau : intermédiaire.** **Technologies imposées :** HDFS, PySpark, Parquet, MongoDB shardé.

### Le problème

Un étudiant cherche des articles sur un sujet. Il veut cinq résultats pertinents, avec le titre, un extrait, la date et le lien vers arXiv. Et vous devez pouvoir prouver que vos résultats sont pertinents.

### Le but du travail

Construire la chaîne d'un moteur de recherche : collecter depuis une API, calculer un index hors ligne avec Spark, servir les requêtes avec MongoDB. Le volume est modeste. Ici, le Big Data, c'est l'architecture : ce qui est calculé une fois à l'avance, et ce qui est fait à chaque requête. Le sujet apprend aussi à mesurer la pertinence, pas seulement la vitesse.

### Les notions Big Data travaillées

| Notion | Ce que vous en faites dans ce sujet | Explication |
| --- | --- | --- |
| Collecte depuis une API | Pagination, pause de 3 s entre deux appels, cache local : on collecte une fois, puis on fige le corpus. | [Architecture](#notion-architecture) |
| Index inversé | Pour chaque mot, la liste des notices qui le contiennent. C'est ce que construit l'index texte de MongoDB. | [Modéliser une base NoSQL](#notion-nosql) |
| Hors ligne, en ligne | Spark calcule les vecteurs TF-IDF une fois ; à la requête, on ne fait que comparer. | [Architecture](#notion-architecture) |
| Pertinence | Precision@5 sur des requêtes jugées à la main : la qualité des résultats se mesure, comme la latence. | [Mesurer](#notion-mesures) |

### Les données

- **Source :** [API arXiv](https://info.arxiv.org/help/api/user-manual.html) et ses [conditions d'utilisation](https://info.arxiv.org/help/api/tou.html). Les métadonnées descriptives, résumés compris, sont en CC0. Les PDF ont des droits distincts : on renvoie vers arXiv, on ne les télécharge pas.
- **Accès :** paginez l'API avec une seule connexion et au moins trois secondes entre deux requêtes. Mettez les réponses en cache, figez la collecte localement, dédoublonnez les versions d'un même identifiant.
- **Volumes :** développement sur 200 notices ; rendu sur 20 000 à 50 000 notices d'un domaine et d'une période fixés. À 2 000 notices par appel et 3 s entre deux appels, la collecte prend moins de deux minutes.

### Ce que vous devez livrer

1. Un corpus collecté, dédoublonné et figé localement : la démonstration se fait sans réseau.
2. Deux méthodes de recherche comparées : l'index textuel de MongoDB et un classement TF-IDF calculé avec Spark.
3. Un écran de résultats avec cinq réponses, leur extrait, leur date et leur lien de provenance.

### Côté technique

Chaîne : API arXiv → HDFS → Spark sur le cluster, TF-IDF → MongoDB shardé + Parquet → recherche.

**Le cluster.** Profils `hdfs`, `spark`, `mongo`. L'index texte de MongoDB fonctionne sur une collection shardée : chaque shard cherche sa part, le routeur fusionne. Mesurez ce que cela coûte.

**Pourquoi MongoDB.** Une notice est un document hétérogène, et MongoDB offre un index textuel sans service de recherche supplémentaire. Document par identifiant arXiv canonique, index texte sur titre et résumé, index (catégorie, date). Les vecteurs TF-IDF restent en Parquet, reliés par identifiant.

**Requêtes à servir :** un sujet, filtré par catégorie et par période, puis l'ouverture de la notice et de sa provenance.

**Expérience à mener :** calculez les vecteurs hors requête. Mesurez la taille de l'index, le temps de construction des caractéristiques et la latence des deux méthodes sur le même corpus.

### Comment je l'évaluerai

- **Démonstration :** une requête précise, une reformulation, une requête hors sujet ; les deux classements côte à côte.
- **Panne à montrer :** arrêtez un shard pendant une recherche : expliquez ce qui répond et ce qui bloque.
- **Indicateurs :** Precision@5 sur vingt requêtes jugées à la main ; latence p95 ; taux de notices dédoublonnées.
- **Protocole :** écrivez les requêtes et les jugements avant le réglage final. Réservez une partie des requêtes au test. Si deux membres jugent différemment, dites-le.
- **Pièges :** TF-IDF est lexical et ne connaît pas les synonymes. 50 000 notices restent un petit corpus : elles servent à apprendre la chaîne ; cela ne prouve pas un passage à l'échelle. Ne prétendez pas le contraire.

### Si vous avez le temps

De petits embeddings calculés localement sur CPU, comparés à TF-IDF sur les mêmes requêtes, avec le modèle utilisé, sa licence et son coût mémoire.

---

<a id="sujet-09"></a>

## Sujet 09 - Énergie : surveiller une consommation en continu

**Niveau : avancé.** **Technologies imposées :** Kafka à trois brokers, Spark Structured Streaming, HDFS, Cassandra à deux nœuds.

### Le problème

Un compteur envoie une mesure par minute. On veut des moyennes glissantes, des alertes quand la consommation s'écarte de la normale, et un historique que l'on peut relire. Tout cela doit survivre à un redémarrage du traitement.

### Le but du travail

Passer du traitement par lots au traitement en flux. Les mesures arrivent une par une, parfois en retard ou en double, et le traitement doit pouvoir s'arrêter et repartir sans rien perdre ni doubler. Le sujet montre que la difficulté du streaming n'est pas la vitesse, mais la justesse quand tout ne se passe pas comme prévu.

### Les notions Big Data travaillées

| Notion | Ce que vous en faites dans ce sujet | Explication |
| --- | --- | --- |
| Vélocité et Kafka | Le producteur publie dans un topic ; Kafka garde les messages et leur offset, ce qui permet de rejouer. | [Kafka](#notion-kafka) |
| Temps de l'événement | On regroupe par l'heure de la mesure, pas l'heure d'arrivée. La watermark dit jusqu'à quand attendre les retardataires. | [Streaming](#notion-streaming) |
| Checkpoint | Spark note les offsets lus et l'état des fenêtres : après un arrêt brutal, il reprend là où il en était. | [Streaming](#notion-streaming) |
| Écriture idempotente | Une clé fixe par fenêtre dans Cassandra : réécrire le même agrégat remplace la ligne, sans doublon. | [Idempotence](#notion-idempotence) |

### Les données

- **Source :** [UCI - Household Power Consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption), CC BY 4.0 (citer Georges Hebrail, Alice Berard et UCI). 2,08 millions de mesures à la minute pour un seul logement, sur quatre ans.
- **Accès :** téléchargez l'archive, gardez les horodatages d'origine, et rejouez les lignes à un débit configurable en ajoutant à chaque mesure un identifiant stable et un instant d'émission.
- **Volumes :** développement sur 10 000 mesures ; rendu : 200 000 mesures rejouées dans le flux, et le fichier complet, 2 millions de mesures, dans HDFS pour le calcul par lots de comparaison.
- **Attention :** un logement n'est pas une ville. Si vous simulez plusieurs capteurs à partir de ce logement, dites-le.

### Ce que vous devez livrer

1. Un producteur Kafka qui rejoue les mesures à un débit réglable.
2. Des fenêtres de cinq minutes et une règle d'alerte que vous savez expliquer, en Spark Structured Streaming.
3. L'historique par capteur et par jour dans Cassandra.

### Côté technique

Chaîne : rejeu UCI → Kafka à trois brokers → Spark Structured Streaming sur le cluster → Cassandra à deux nœuds → courbes ; checkpoint dans HDFS.

**Le cluster.** Profils `hdfs`, `spark`, `kafka`, `cassandra`. Topic à 3 partitions et 2 copies. C'est la pile la plus lourde : il faut un PC de 16 Go.

**Pourquoi Cassandra.** Des écritures continues et des lectures par (capteur, jour) : table partitionnée par capteur et jour, triée par horodatage puis identifiant. Pour les agrégats, une clé déterministe (capteur, jour, début de fenêtre) que l'on réécrit à l'identique en cas de rejeu, sans créer de doublon.

**Requêtes à servir :** une journée de mesures d'un capteur ; ses dernières fenêtres. Sans parcourir toute la table.

**Expérience à mener :** injectez des doublons et des retards dans le flux. Arrêtez le traitement brutalement, relancez-le sur son checkpoint, et comparez les agrégats obtenus à un calcul batch sur les mêmes données.

### Comment je l'évaluerai

- **Démonstration :** un pic de consommation, un événement en retard, un arrêt puis une reprise, et la comparaison flux / batch.
- **Panne à montrer :** tuez le traitement en flux puis relancez-le : aucun événement perdu ni compté deux fois. Arrêtez ensuite un nœud Cassandra et montrez ce que deviennent les écritures.
- **Indicateurs :** événements traités par seconde ; délai de bout en bout p95 ; écart entre agrégats du flux et agrégats batch.
- **Protocole :** fixez la watermark et la politique pour les événements au-delà. Un doublon ne compte qu'une fois. Le délai se mesure depuis l'émission par le producteur, pas depuis la date historique de la mesure.
- **Pièges :** un pic n'est pas une panne. Les événements écartés par la watermark doivent être comptés et expliqués. Ne promettez pas l'exactly-once de bout en bout si vous ne l'avez pas démontré.

### Si vous avez le temps

Un détecteur d'anomalies comparé à votre règle, sur des perturbations injectées et étiquetées.

---

<a id="sujet-10"></a>

## Sujet 10 - Qissaria : compter les événements web en direct

**Niveau : avancé.** **Technologies imposées :** Kafka à trois brokers, Spark Structured Streaming, HDFS, Redis Cluster.

### Le problème

Qissaria, la place de marché fictive des TP, veut voir en direct ses vues, ajouts au panier et achats, et ses produits les plus consultés. Les compteurs doivent rester justes même si le traitement s'interrompt et reprend.

### Le but du travail

Le même passage au flux que le sujet 09, avec des compteurs lus en direct par un tableau de bord. L'enjeu est la justesse : après une panne et une reprise, chaque événement doit compter une fois et une seule. Redis rend la difficulté visible, car l'opération la plus naturelle, l'incrément, est justement celle qui ne se rejoue pas.

### Les notions Big Data travaillées

| Notion | Ce que vous en faites dans ce sujet | Explication |
| --- | --- | --- |
| Partitions Kafka | Un topic est découpé en partitions, lues en parallèle. L'ordre n'est garanti qu'à l'intérieur d'une partition. | [Kafka](#notion-kafka) |
| État des fenêtres | Spark garde en mémoire les compteurs des fenêtres ouvertes ; la watermark lui permet de les libérer. | [Streaming](#notion-streaming) |
| Écriture par micro-lot | `foreachBatch` livre chaque micro-lot avec son numéro : de quoi écrire dans Redis de façon rejouable. | [Streaming](#notion-streaming) |
| `INCR` ou `SET` | Un incrément rejoué compte deux fois. Écrire la valeur recalculée donne le même résultat à chaque rejeu. | [Idempotence](#notion-idempotence) |

### Les données

- **Source :** le clickstream du cours, décrit dans [data/README.md](https://github.com/M2P-git/tp-big-data/blob/main/data/README.md) du dépôt des TP. Format identique au jeu public REES46, données entièrement synthétiques.
- **Accès :** le script [scripts/generer_clickstream.py](https://github.com/M2P-git/tp-big-data/blob/main/scripts/generer_clickstream.py) du dépôt des TP, avec ses options `--lignes` et `--graine`. Donnez à chaque événement un identifiant stable dérivé du fichier et du numéro de ligne.
- **Volumes :** développement sur les 5 000 événements de l'échantillon du dépôt ; rendu sur un million d'événements générés au moins, 3 millions conseillés. Le fichier de TP de 11 millions de lignes est facultatif.
- **Attention :** un format inspiré de REES46 ne rend pas ces événements réels. Dites-le dans le rapport.

### Ce que vous devez livrer

1. Un producteur Kafka qui rejoue les événements en conservant leur horodatage métier.
2. Par fenêtre : vues, paniers, achats et top produits, en Spark Structured Streaming.
3. Ces agrégats servis dans Redis, et un affichage de l'état du traitement.

### Côté technique

Chaîne : clickstream → Kafka à trois brokers → Spark Structured Streaming sur le cluster → Redis Cluster → compteurs ; checkpoint dans HDFS.

**Le cluster.** Profils `hdfs`, `spark`, `kafka`, `redis`. L'exemple `flux_compteurs.py` du cluster est votre point de départ : il compte déjà par fenêtre, mais il ne dédoublonne pas et ne sert pas le top produits.

**Pourquoi Redis.** Des compteurs lus en permanence par un tableau de bord, avec une durée de vie : clés par (fenêtre, type d'événement), ensembles ordonnés pour le top produits. On écrit des valeurs absolues recalculées par Spark, jamais des incréments.

**Requêtes à servir :** une fenêtre et son top produits ; savoir si une fenêtre est close ou encore susceptible de changer.

**Expérience à mener :** rejouez le même lot après un arrêt du consommateur. Les compteurs doivent être identiques à ceux d'un calcul batch sur le même fichier.

### Comment je l'évaluerai

- **Démonstration :** vous lancez le flux, vous arrêtez le consommateur, vous reprenez, et vous rapprochez les compteurs du calcul batch.
- **Panne à montrer :** tuez le flux, relancez-le, et comparez chaque compteur au calcul par lots : ils doivent être égaux.
- **Indicateurs :** débit soutenu ; délai p95 depuis l'émission ; nombre de doublons et de retards observés ; écart avec le batch.
- **Protocole :** fenêtres, watermark et expiration Redis écrits noir sur blanc avant la démonstration.
- **Pièges :** un `INCR` Redis rejoué à la reprise d'un micro-lot compte deux fois. L'offset Kafka, le checkpoint Spark et l'écriture Redis ne forment pas une transaction : documentez les cas testés. Le ratio achats / vues n'est pas un taux de conversion par session.

### Si vous avez le temps

Un suivi des sessions et des paniers abandonnés, avec un état par session, des délais d'expiration et un traitement explicite des événements tardifs.

---

## Rendu et évaluation

### Les quatre jalons

| Jalon | Ce que je veux voir |
| --- | --- |
| 1. Cadrer | Données téléchargées et inspectées, architecture dessinée, trois requêtes NoSQL écrites, tâches réparties |
| 2. Faire passer un extrait | Un petit extrait traverse toute la chaîne, sur le cluster, et produit une sortie consultable |
| 3. Monter en volume | Le volume du rendu, les rejets, la référence, les mesures, les cas d'erreur, la reprise pour les sujets en flux |
| 4. Livrer | Installation depuis un environnement propre, démonstration répétée, rapport, dépôt, contributions |

### Ce que vous rendez

- **Un dépôt Git** : code, versions des dépendances fixées, configuration d'exemple, commandes de lancement et d'acquisition des données. Ni mot de passe, ni fichier de plusieurs Go. Un jeu soumis à restrictions reste téléchargeable par script, pas distribué.
- **Les données tracées** : lien, licence, date, script, dictionnaire des colonnes. Un petit jeu de démonstration autorisé.
- **Des contrôles** : un agrégat recalculé à la main sur un petit extrait, l'unicité des clés, les totaux conservés d'un bout à l'autre, une relance sans doublons. Pour un modèle, les découpages et les scores de la référence.
- **Un rapport de 6 à 10 pages** : le besoin et le périmètre ; l'architecture et le modèle NoSQL ; les expériences et leurs chiffres ; les résultats ; les limites ; qui a fait quoi.
- **Une démonstration qui tourne** sans réseau, et une vidéo de 2 à 3 minutes en secours.
- **6 à 8 diapositives** pour la soutenance.

### Le barème, sur 20

| Critère | Points |
| --- | ---: |
| Données : acquisition, qualité, provenance, règles de nettoyage | 4 |
| Spark et HDFS sur le cluster : traitements corrects, Parquet, partitionnement, pas de `collect()` abusif | 4 |
| NoSQL en cluster : choix justifié, clés, répartition entre les nœuds, requêtes, mesures | 4 |
| Validation : référence, protocole, limites annoncées | 3 |
| Démonstration, panne en direct et réponses à l'oral | 3 |
| Reproductibilité, documentation, contributions individuelles | 2 |
| **Total** | **20** |

Le socle de chaque sujet permet d'avoir 20. L'extension n'apporte des points que si elle est faite et évaluée aussi sérieusement que le socle. Chaque membre de l'équipe répond à une question technique et montre une contribution identifiable dans le dépôt.

**Sans Spark sur le cluster et sans base NoSQL réellement utilisée, le projet n'est pas évalué.**

### La soutenance : 8 minutes, questions comprises

1. **1 minute** : le problème, pour qui, avec quelles données.
2. **2 minutes** : l'architecture, la répartition sur le cluster, pourquoi cette base.
3. **2 minutes** : la démonstration, avec une panne en direct.
4. **1 minute** : les résultats face à la référence, et les limites.
5. **2 minutes** : questions ; chaque membre répond à une question technique.

Questions que je poserai sûrement : avec dix fois plus de données, qu'est-ce qui casse en premier ? Pourquoi cette base et pas celle du sujet voisin ? Que se passe-t-il si je relance votre pipeline deux fois ?

### Ce qui fait perdre des points

- Spark importé, puis tout converti en pandas à la deuxième cellule.
- Une base NoSQL remplie une fois et jamais interrogée depuis l'application.
- Des chiffres sans contexte : « c'est plus rapide » sans dire combien, sur quelle machine, combien de fois.
- Un modèle évalué sur ses données d'entraînement, ou découpé au hasard sur une série temporelle.
- Une démonstration qui a besoin d'internet ou d'un compte, ou que personne d'autre dans l'équipe ne sait relancer.
- Spark lancé en mode local, ou des fichiers lus sur le disque au lieu de HDFS.
- Un rapport où l'on ne sait pas qui a fait quoi.

## Rappel sur les indicateurs

- **p95 de latence** : 95 % des délais observés sont inférieurs ou égaux à cette valeur. Dites comment vous mesurez et sur combien d'observations.
- **MAE** : moyenne des erreurs absolues, dans l'unité de la cible. Toujours comparée à une règle simple sur le même jeu.
- **Precision@5** : proportion de résultats pertinents parmi les cinq premiers, moyennée sur les requêtes de test.
- **Recall@10** : part des films pertinents du test retrouvés dans les dix recommandations. Définissez le seuil de pertinence et les utilisateurs évaluables.
- **Macro-F1** : moyenne non pondérée des F1 de chaque classe. Joignez la répartition des classes et la matrice de confusion.
- **Précision et rappel d'une alerte** : part des alertes qui correspondent à un scénario étiqueté ; part des scénarios étiquetés qui ont déclenché une alerte. Sur données synthétiques, ces chiffres ne valent que pour votre générateur.

## Le projet sur votre CV

Une fois le projet terminé, il a sa place sur votre CV et dans un entretien. Nommez ce que vous avez livré (un pipeline, un moteur, un service), donnez vos chiffres réels (volume, durée, latence ou score, avec la machine et la référence), dites ce que vous avez fait vous-même, et mettez le lien du dépôt. Un résultat obtenu sur des données simulées se présente comme tel.
