"""Écrire des classements Spark dans Redis Cluster, de façon rejouable.

Top 10 des produits vus chaque jour, rangé dans un ensemble ordonné par jour.
Chaque clé est remplacée en entier (DEL puis ZADD dans une transaction) :
relancer le script redonne exactement le même contenu.

    spark-submit /home/jovyan/exemples/vers_redis.py /brut/clickstream.csv
"""
import sys
from collections import Counter

from pyspark.sql import SparkSession, Window, functions as F
from redis.cluster import ClusterNode, RedisCluster

# Plusieurs points d'entrée : si l'un est arrêté, le client passe par un autre.
NOEUD = {"startup_nodes": [ClusterNode(f"redis{i}", 6379) for i in range(1, 7)]}
chemin = sys.argv[1] if len(sys.argv) > 1 else "/brut/clickstream.csv"

spark = SparkSession.builder.appName("vers-redis").getOrCreate()
vues = (spark.read.csv(chemin, header=True)
        .where(F.col("event_type") == "view")
        .withColumn("jour", F.substring("event_time", 1, 10))
        .groupBy("jour", "product_id").count())
rang = Window.partitionBy("jour").orderBy(F.desc("count"), "product_id")
top = (vues.withColumn("rang", F.row_number().over(rang)).where("rang <= 10")
       .groupBy("jour").agg(F.collect_list(F.struct("product_id", "count")).alias("produits")))


def ecrire(lignes):
    """Exécutée sur les workers, une fois par partition."""
    from redis.cluster import ClusterNode, RedisCluster
    r = RedisCluster(startup_nodes=[ClusterNode(f"redis{i}", 6379) for i in range(1, 7)])
    for ligne in lignes:
        cle = f"top:vues:{ligne.jour}"
        transaction = r.pipeline(transaction=True)
        transaction.delete(cle)
        transaction.zadd(cle, {p.product_id: p["count"] for p in ligne.produits})
        transaction.execute()
    r.close()


top.foreachPartition(ecrire)

r = RedisCluster(**NOEUD)
cles = sorted(r.scan_iter(match="top:vues:*", target_nodes=RedisCluster.PRIMARIES))
print("Classements écrits :", len(cles))
print("Top 3 du", cles[0].decode()[-10:], ":", r.zrevrange(cles[0], 0, 2, withscores=True))
# Le hachage de chaque clé désigne l'un des trois nœuds principaux.
repartition = Counter(r.get_node_from_key(cle).name for cle in cles)
for noeud, nombre in sorted(repartition.items()):
    print(f"  nœud {noeud} : {nombre} clés")
spark.stop()
