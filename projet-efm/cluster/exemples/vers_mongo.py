"""Écrire un agrégat Spark dans MongoDB shardé, de façon rejouable.

Chaque worker écrit ses propres partitions dans MongoDB : les données ne
repassent pas par le driver. L'écriture remplace chaque document par sa clé,
donc relancer le script ne crée aucun doublon.

    spark-submit /home/jovyan/exemples/vers_mongo.py /brut/clickstream.csv
"""
import sys

from pymongo import MongoClient
from pyspark.sql import SparkSession, functions as F

URI = "mongodb://mongo-router:27017"
chemin = sys.argv[1] if len(sys.argv) > 1 else "/brut/clickstream.csv"

client = MongoClient(URI)
if "clients" not in client.projet.list_collection_names():
    # La clé de sharding décide sur quel shard vit chaque document.
    # Hachée, elle répartit les clients au hasard et de façon équilibrée.
    client.admin.command("shardCollection", "projet.clients", key={"_id": "hashed"})

spark = SparkSession.builder.appName("vers-mongo").getOrCreate()
profils = (spark.read.csv(chemin, header=True)
           .groupBy("user_id")
           .agg(F.count("*").alias("evenements"),
                F.sum(F.when(F.col("event_type") == "purchase", 1).otherwise(0)).alias("achats")))


def ecrire(lignes):
    """Exécutée sur les workers, une fois par partition."""
    from pymongo import MongoClient, ReplaceOne
    connexion = MongoClient(URI)
    collection = connexion.projet.clients
    lot = []
    for ligne in lignes:
        document = {"_id": ligne.user_id, "evenements": ligne.evenements, "achats": ligne.achats}
        lot.append(ReplaceOne({"_id": ligne.user_id}, document, upsert=True))
        if len(lot) == 1000:
            collection.bulk_write(lot, ordered=False)
            lot = []
    if lot:
        collection.bulk_write(lot, ordered=False)
    connexion.close()


profils.foreachPartition(ecrire)

print("Documents dans projet.clients :", client.projet.clients.count_documents({}))
for shard in client.projet.clients.aggregate([{"$collStats": {"count": {}}}]):
    print(f"  {shard['shard']} : {shard['count']} documents")

spark.stop()
