"""Compter des événements Kafka par fenêtre de 5 minutes et servir les compteurs dans Redis.

- Temps de l'événement : on regroupe selon event_time, pas selon l'heure d'arrivée.
- Watermark : on accepte 10 minutes de retard ; au-delà, la fenêtre est fermée.
- Checkpoint dans HDFS : après un arrêt, le flux reprend là où il en était.
- Écriture rejouable : on écrit la valeur complète de chaque compteur (SET), jamais
  un incrément. Un micro-lot rejoué après une panne réécrit donc les mêmes valeurs.

    spark-submit /home/jovyan/exemples/flux_compteurs.py --topic clics --duree 120
"""
import argparse
import time

from pyspark.sql import SparkSession, functions as F, types as T
from redis.cluster import ClusterNode, RedisCluster

parser = argparse.ArgumentParser()
parser.add_argument("--topic", default="clics")
parser.add_argument("--duree", type=int, default=0, help="secondes avant arrêt ; 0 = sans fin")
args = parser.parse_args()

ENTREES = [ClusterNode(f"redis{i}", 6379) for i in range(1, 7)]

spark = SparkSession.builder.appName("flux-compteurs").getOrCreate()
schema = T.StructType([T.StructField(nom, T.StringType()) for nom in
                       ["event_time", "event_type", "product_id", "user_id"]])

evenements = (spark.readStream.format("kafka")
              .option("kafka.bootstrap.servers", "kafka1:9092,kafka2:9092,kafka3:9092")
              .option("subscribe", args.topic)
              .option("startingOffsets", "earliest")
              .load()
              .select(F.from_json(F.col("value").cast("string"), schema).alias("e"))
              .select(F.to_timestamp(F.substring("e.event_time", 1, 19)).alias("instant"),
                      F.col("e.event_type").alias("type")))

compteurs = (evenements
             .withWatermark("instant", "10 minutes")
             .groupBy(F.window("instant", "5 minutes"), "type")
             .count())


def ecrire(lot, numero_lot):
    """Appelée à chaque micro-lot avec les compteurs modifiés (mode update)."""
    lignes = lot.collect()        # quelques dizaines de lignes : les compteurs, pas les événements
    r = RedisCluster(startup_nodes=ENTREES)
    for ligne in lignes:
        debut = ligne.window.start.strftime("%Y-%m-%dT%H:%M")
        r.set(f"compteur:{debut}:{ligne.type}", ligne["count"], ex=86400)
    r.close()
    print(f"micro-lot {numero_lot} : {len(lignes)} compteurs écrits", flush=True)


requete = (compteurs.writeStream
           .outputMode("update")
           .foreachBatch(ecrire)
           .option("checkpointLocation", f"/checkpoints/flux_compteurs_{args.topic}")
           .trigger(processingTime="5 seconds")
           .start())

if args.duree > 0:
    requete.awaitTermination(args.duree)
    # On laisse finir le micro-lot en cours avant d'arrêter. Un arrêt en plein lot ne
    # perd rien, puisque le lot est rejoué à la relance, mais il remplit le journal d'erreurs.
    while requete.status["isTriggerActive"]:
        time.sleep(0.5)
    requete.stop()
else:
    requete.awaitTermination()
spark.stop()
