"""Écrire un agrégat Spark dans Cassandra, de façon rejouable.

Nombre d'événements par type et par jour. La clé primaire est déterministe :
réécrire la même ligne la remplace, donc relancer le script ne crée aucun doublon.

    spark-submit /home/jovyan/exemples/vers_cassandra.py /brut/clickstream.csv
"""
import sys

from cassandra.cluster import Cluster
from pyspark.sql import SparkSession, functions as F

NOEUDS = ["cassandra1", "cassandra2"]
chemin = sys.argv[1] if len(sys.argv) > 1 else "/brut/clickstream.csv"

session = Cluster(NOEUDS).connect()
# Deux copies de chaque partition, sur deux nœuds différents.
session.execute("""CREATE KEYSPACE IF NOT EXISTS projet
                   WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2}""")
# Clé de partition : le type d'événement. Clé de tri : le jour.
session.execute("""CREATE TABLE IF NOT EXISTS projet.evenements_par_jour (
                     event_type text, jour date, nombre bigint,
                     PRIMARY KEY ((event_type), jour))""")

spark = SparkSession.builder.appName("vers-cassandra").getOrCreate()
par_jour = (spark.read.csv(chemin, header=True)
            .withColumn("jour", F.to_date(F.substring("event_time", 1, 10)))
            .groupBy("event_type", "jour").count())


def ecrire(lignes):
    """Exécutée sur les workers, une fois par partition."""
    from cassandra.cluster import Cluster
    connexion = Cluster(NOEUDS)
    s = connexion.connect("projet")
    requete = s.prepare("INSERT INTO evenements_par_jour (event_type, jour, nombre) VALUES (?, ?, ?)")
    for ligne in lignes:
        s.execute(requete, (ligne.event_type, ligne.jour, ligne["count"]))
    connexion.shutdown()


par_jour.foreachPartition(ecrire)

lignes = session.execute("SELECT count(*) FROM projet.evenements_par_jour").one()[0]
print("Lignes dans projet.evenements_par_jour :", lignes)
achats = session.execute("SELECT jour, nombre FROM projet.evenements_par_jour "
                         "WHERE event_type = 'purchase' LIMIT 3")
for ligne in achats:
    print(" ", ligne.jour, ligne.nombre, "achats")
spark.stop()
