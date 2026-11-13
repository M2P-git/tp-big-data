"""Premier traitement sur le cluster.

Vérifie que Spark lit un fichier dans HDFS, répartit le calcul sur les deux
workers et écrit du Parquet partitionné dans HDFS. Lancer depuis un terminal
Jupyter, après avoir chargé le fichier dans HDFS (voir le README du cluster) :

    python /home/jovyan/exemples/premier_job.py /brut/clickstream.csv
"""
import json
import sys
import time
import urllib.request

from pyspark.sql import SparkSession, functions as F

chemin = sys.argv[1] if len(sys.argv) > 1 else "/brut/clickstream.csv"

spark = SparkSession.builder.appName("premier-job").getOrCreate()
sc = spark.sparkContext
print("Master :", sc.master)

debut = time.time()
df = spark.read.csv(chemin, header=True)
print("Partitions lues :", df.rdd.getNumPartitions(), "(une par bloc HDFS de 16 Mo)")

# Un groupBy : map sur chaque partition, shuffle entre les workers, puis reduce.
(df.groupBy("event_type")
   .agg(F.count("*").alias("evenements"), F.countDistinct("user_id").alias("clients"))
   .orderBy("event_type")
   .show())

# Écriture rejouable : overwrite remplace le résultat précédent au lieu de l'ajouter.
(df.withColumn("jour", F.to_date(F.substring("event_time", 1, 10)))
   .write.mode("overwrite").partitionBy("jour").parquet("/propre/clickstream"))
print(f"Durée totale : {time.time() - debut:.1f} s")

# Qui a travaillé ? L'API de l'application Spark liste les exécuteurs et leurs tâches.
url = f"{sc.uiWebUrl}/api/v1/applications/{sc.applicationId}/executors"
for executeur in json.load(urllib.request.urlopen(url)):
    if executeur["id"] != "driver":
        print(f"Exécuteur {executeur['id']} ({executeur['hostPort']}) : "
              f"{executeur['totalTasks']} tâches, {executeur['totalCores']} cœurs")

spark.stop()
