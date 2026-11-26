"""Démonstrations de la séance S5 (Spark et PySpark), mêmes programmes que les notebooks des étudiants.

Le profil spark doit tourner (docker compose --profile spark up -d). Depuis la racine du dépôt :
    docker compose exec jupyter-spark python work/tp/s5/spark_demo.py verifier
    docker compose exec jupyter-spark python work/tp/s5/spark_demo.py duel --entree hdfs://namenode:8020/qissaria/clickstream/clickstream_aout.csv
Sur une seule machine (image pyspark-notebook seule, ou PySpark + Java installés), depuis la racine du dépôt :
    DEPOT_TP=. python spark_demo.py tout --local

La connexion au cluster ne figure pas dans le code : le conteneur jupyter-spark la fournit par la variable
PYSPARK_SUBMIT_ARGS (master, adresse du driver, cœurs). Sans elle, Spark démarre en local.
"""
import argparse
import json
import os
import re
import time
import urllib.request
from pathlib import Path

# Le dépôt des TP est monté en /home/jovyan/work dans les quatre conteneurs Spark.
DEPOT = Path(os.environ.get("DEPOT_TP", "/home/jovyan/work")).resolve()
PETIT_CSV = (DEPOT / "data" / "echantillon" / "clickstream_petit.csv").as_uri()
AOUT_CSV = (DEPOT / "data" / "clickstream_aout.csv").as_uri()
AOUT_HDFS = "hdfs://namenode:8020/qissaria/clickstream/clickstream_aout.csv"
ECHANTILLON = (DEPOT / "data" / "echantillon").as_uri()
PARQUET = (DEPOT / "sorties" / "clickstream_aout_parquet").as_uri()
PARQUET_HDFS = "hdfs://namenode:8020/qissaria/parquet/clickstream_aout"


def creer_session(nom="Qissaria-S5", local=False):
    """La même session que la première cellule du notebook."""
    from pyspark.sql import SparkSession
    constructeur = (SparkSession.builder
                    .appName(nom)
                    .config("spark.sql.shuffle.partitions", "4")     # 4 partitions après un shuffle
                    .config("spark.sql.adaptive.enabled", "false")   # plan lu tel quel (partie 4 : AQE)
                    .config("spark.ui.showConsoleProgress", "false"))  # sorties lisibles dans le terminal
    if local:
        constructeur = constructeur.master("local[2]")
    spark = constructeur.getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def lire(spark, chemin=PETIT_CSV):
    return spark.read.option("header", True).csv(chemin)


def enrichir(df):
    """Partie 2 : le prix en nombre, le rayon (1er mot de category_code) et le jour."""
    from pyspark.sql import functions as F
    return (df.withColumn("prix", F.col("price").cast("double"))
              .withColumn("rayon", F.split("category_code", r"\.").getItem(0))
              .withColumn("jour", F.to_date(F.substring("event_time", 1, 10))))


def nombre_jobs(spark):
    """Jobs lancés depuis l'ouverture de la session (tous sans groupe ici)."""
    return len(spark.sparkContext.statusTracker().getJobIdsForGroup(None))


def attendre_executors(spark, nombre=2, delai=30):
    """Sur un cluster, les executors s'enregistrent quelques secondes après l'ouverture de la session."""
    sc = spark.sparkContext
    if not sc.master.startswith("spark://"):
        return
    for _ in range(delai):
        # la liste contient le driver et chaque executor enregistré
        if sc._jsc.sc().getExecutorMemoryStatus().size() - 1 >= nombre:
            return
        time.sleep(1)


def executors(spark):
    """Les executors déclarés auprès du driver, lus dans l'API de l'interface 4040."""
    sc = spark.sparkContext
    if not sc.uiWebUrl:
        return
    url = f"http://127.0.0.1:{sc.uiWebUrl.rsplit(':', 1)[1]}/api/v1/applications/{sc.applicationId}/executors"
    try:
        with urllib.request.urlopen(url, timeout=10) as reponse:
            etats = json.load(reponse)
    except (OSError, ValueError) as erreur:
        print("Métadonnées de l'interface indisponibles :", erreur)
        return
    for etat in etats:
        role = "driver  " if etat["id"] == "driver" else f"executor {etat['id']}"
        print(f"{role} : {etat['hostPort']:<24} coeurs={etat['totalCores']}  tâches={etat['totalTasks']}")


def stages(spark, depuis):
    """Les stages terminés des jobs numérotés à partir de depuis : tâches, lecture, shuffle (API de l'interface 4040)."""
    sc = spark.sparkContext
    api = f"http://127.0.0.1:{sc.uiWebUrl.rsplit(':', 1)[1]}/api/v1/applications/{sc.applicationId}"
    liste = json.load(urllib.request.urlopen(api + "/jobs"))
    par_id = {s["stageId"]: s for s in json.load(urllib.request.urlopen(api + "/stages"))}
    for job in sorted(liste, key=lambda j: j["jobId"]):
        if job["jobId"] < depuis:
            continue
        for sid in sorted(job["stageIds"]):
            st = par_id.get(sid)
            if st and st["status"] == "COMPLETE":
                print(f"job {job['jobId']}, stage {sid} : {st['numTasks']} tâches, {st['inputBytes'] / 1e6:.0f} Mo lus, "
                      f"shuffle écrit {st['shuffleWriteBytes'] / 1e3:.0f} Ko, temps cumulé des tâches {st['executorRunTime'] / 1000:.1f} s")


def chrono(nom, resultat, lignes=10):
    """Affiche un résultat et le temps de l'action qui le calcule."""
    debut = time.perf_counter()
    resultat.show(lignes, truncate=False)
    print(f"{nom} : {time.perf_counter() - debut:.1f} s\n")


def demontrer(spark, mode, chemin):
    from pyspark.sql import functions as F
    sc = spark.sparkContext
    # ---------------------------------------------------------------- partie 1
    if mode in ("verifier", "tout"):
        attendre_executors(spark)
        print("Version Spark :", spark.version)
        print("Master        :", sc.master)
        print("Application   :", sc.applicationId)
        print("Interface     : http://localhost:4040")
        print("Parallélisme  :", sc.defaultParallelism, "coeurs disponibles")
        executors(spark)
    if mode in ("verifier", "lire", "tout"):
        df = lire(spark, chemin)
        df.printSchema()
        df.select("event_time", "event_type", "brand", "user_id").show(5, truncate=False)
        print("Lignes :", df.count())
    if mode in ("rdd", "tout"):
        df = lire(spark, chemin)
        lignes = sc.textFile(chemin)
        entete = lignes.first()
        print("RDD : des lignes de texte, sans schéma. Une ligne :", lignes.take(2)[1])
        types_rdd = (lignes.filter(lambda l: l != entete)
                           .map(lambda l: (l.split(",")[1], 1))
                           .reduceByKey(lambda a, b: a + b))
        print("RDD       :", sorted(types_rdd.collect()))
        types_df = df.groupBy("event_type").count().orderBy("event_type")
        print("DataFrame :", [(r["event_type"], r["count"]) for r in types_df.collect()])
    if mode in ("paresseux", "tout"):
        depart = nombre_jobs(spark)
        df = lire(spark, chemin)
        print(f"  après read.csv          : {nombre_jobs(spark) - depart} job(s)")
        achats = df.filter(F.col("event_type") == "purchase")
        print(f"  après filter            : {nombre_jobs(spark) - depart} job(s)")
        par_marque = achats.groupBy("brand").count()
        print(f"  après groupBy().count() : {nombre_jobs(spark) - depart} job(s)")
        par_marque.explain()
        print(f"  après explain()         : {nombre_jobs(spark) - depart} job(s)")
        par_marque.orderBy(F.desc("count")).show()
        print(f"  après show()            : {nombre_jobs(spark) - depart} job(s)")
        print("  count() renvoie         :", par_marque.count())
        print(f"  après count()           : {nombre_jobs(spark) - depart} job(s)")
    if mode in ("plan", "tout"):
        df = lire(spark, chemin)
        par_marque = df.filter(F.col("event_type") == "purchase").groupBy("brand").count()
        print("Plan physique, à lire de bas en haut :")
        par_marque.explain()
        print("Partitions de lecture :", df.rdd.getNumPartitions(),
              "| partitions après l'échange :", par_marque.rdd.getNumPartitions())
    if mode in ("interface", "tout"):
        df = lire(spark, chemin)
        df.filter(F.col("event_type") == "purchase").groupBy("brand").count().orderBy(F.desc("count")).show()
        executors(spark)
    # ---------------------------------------------------------------- partie 2
    if mode in ("colonnes", "tout"):
        ev = enrichir(lire(spark, chemin))
        ev.select("event_type", "brand", "price", "prix", "rayon", "jour").show(5)
        gamme = F.when(F.col("prix") >= 1000, "haut").when(F.col("prix") >= 300, "milieu").otherwise("entrée")
        ev.withColumn("gamme", gamme).groupBy("gamme").count().orderBy(F.desc("count")).show()
    if mode in ("agreger", "tout"):
        ev = enrichir(lire(spark, chemin))
        achats = ev.filter((F.col("event_type") == "purchase") & F.col("brand").isNotNull())
        (achats.groupBy("brand")
               .agg(F.count("*").alias("achats"), F.sum("prix").alias("chiffre"),
                    F.avg("prix").alias("prix_moyen"), F.countDistinct("user_id").alias("clients"))
               .orderBy(F.desc("chiffre")).show())
        (ev.filter(F.col("brand").isNotNull())
           .groupBy("brand").pivot("event_type", ["view", "cart", "purchase"]).count().fillna(0)
           .withColumn("conversion", F.round(F.col("purchase") / F.col("view"), 2))
           .orderBy("brand").show())
    if mode == "duel":
        df = lire(spark, chemin)
        print("Fichier :", chemin)
        print("Partitions de lecture :", df.rdd.getNumPartitions())
        chrono("Événements par type", df.groupBy("event_type").count().orderBy("event_type"))
        chrono("Top 10 des marques achetées",
               df.filter((F.col("event_type") == "purchase") & F.col("brand").isNotNull())
                 .groupBy("brand").count().orderBy(F.desc("count"), F.asc("brand")).limit(10))
    if mode == "cinq":
        ev = enrichir(lire(spark, chemin))
        marque = F.col("brand").isNotNull()
        chrono("1. Événements par type", ev.groupBy("event_type").count().orderBy("event_type"))
        chrono("2. Top 5 des marques achetées",
               ev.filter((F.col("event_type") == "purchase") & marque)
                 .groupBy("brand").count().orderBy(F.desc("count"), "brand").limit(5), 5)
        chrono("3. Top 5 des marques consultées",
               ev.filter((F.col("event_type") == "view") & marque)
                 .groupBy("brand").count().orderBy(F.desc("count"), "brand").limit(5), 5)
        chrono("4. Chiffre d'affaires par rayon (top 5)",
               ev.filter(F.col("event_type") == "purchase").groupBy("rayon")
                 .agg(F.count("*").alias("achats"), F.round(F.sum("prix")).cast("long").alias("chiffre"))
                 .orderBy(F.desc("chiffre")).limit(5), 5)
        chrono("5. Clients distincts par jour (5 premiers jours)",
               ev.groupBy("jour").agg(F.countDistinct("user_id").alias("clients")).orderBy("jour").limit(5), 5)

    # ---------------------------------------------------------------- partie 3
    if mode in ("sql", "tout"):
        ev = enrichir(lire(spark, chemin))
        ev.createOrReplaceTempView("evenements")
        top_sql = spark.sql("""
            SELECT brand, COUNT(*) AS achats FROM evenements
            WHERE event_type = 'purchase' AND brand IS NOT NULL
            GROUP BY brand ORDER BY achats DESC, brand LIMIT 10""")
        top_sql.show()
        top_df = (ev.filter((F.col("event_type") == "purchase") & F.col("brand").isNotNull())
                    .groupBy("brand").agg(F.count("*").alias("achats")).orderBy(F.desc("achats"), "brand").limit(10))
        print("exceptAll dans les deux sens :", top_sql.exceptAll(top_df).count(), top_df.exceptAll(top_sql).count())
        spark.sql("""
            SELECT brand, COUNT(*) AS paniers FROM evenements
            WHERE event_type = 'cart' AND brand IS NOT NULL
            GROUP BY brand HAVING COUNT(*) >= 2 ORDER BY brand""").show()
    if mode in ("jointure", "tout"):
        ev = enrichir(lire(spark, chemin))
        cat = spark.read.option("header", True).csv(ECHANTILLON + "/catalogue_petit.csv")
        dbl = spark.read.option("header", True).csv(ECHANTILLON + "/catalogue_doublon.csv")
        print("Lignes : interne", ev.join(cat, "product_id").count(), "| gauche", ev.join(cat, "product_id", "left").count(),
              "| gauche avec le catalogue en double", ev.join(dbl, "product_id", "left").count())
        (ev.join(dbl, "product_id", "left").filter(F.col("event_type") == "purchase")
           .groupBy("brand").agg(F.count("*").alias("achats"), F.sum("prix").alias("chiffre")).orderBy("brand").show())
        print("Clés en double dans le catalogue :")
        dbl.groupBy("product_id").count().filter("count > 1").show()
    if mode == "rapport":
        rayons = spark.read.option("header", True).csv(ECHANTILLON + "/rayons.csv")
        rapport = (enrichir(lire(spark, chemin)).filter(F.col("event_type") == "purchase")
                   .join(rayons, "rayon", "left").groupBy("rayon", "libelle", "responsable")
                   .agg(F.round(F.sum("prix")).cast("long").alias("chiffre"),
                        F.round(F.sum(F.col("prix") * F.col("marge"))).cast("long").alias("marge"))
                   .orderBy(F.desc("chiffre")))
        print("Dans le plan :")
        for ligne in rapport._jdf.queryExecution().executedPlan().toString().splitlines():
            if "Broadcast" in ligne:
                print("  ", ligne.strip(" +-:*").split(", [plan_id")[0])
        chrono("Rapport par rayon", rapport, 12)
    if mode == "parquet":
        sortie = PARQUET_HDFS if chemin.startswith("hdfs:") else PARQUET
        ev = enrichir(lire(spark, chemin))
        debut = time.perf_counter()
        (ev.select("event_time", "event_type", "product_id", "brand", "prix", "user_id", "rayon", "jour")
           .repartition("jour").write.mode("overwrite").partitionBy("jour").parquet(sortie))
        print(f"Écriture de {sortie} : {time.perf_counter() - debut:.0f} s")
        pq = spark.read.parquet(sortie)
        le_15 = (pq.filter(F.col("jour") == "2026-08-15").filter(F.col("event_type") == "purchase")
                   .groupBy("rayon").agg(F.round(F.sum("prix")).cast("long").alias("chiffre")).orderBy(F.desc("chiffre")))
        plan = le_15._jdf.queryExecution().executedPlan().toString()
        print("Dans le plan :", re.search(r"PartitionFilters: \[[^\]]*\]", plan).group(0))
        chrono("Le 15 août, par rayon (Parquet)", le_15, 5)
        csv = lire(spark, chemin)
        chrono("Événements du 15 août, CSV", csv.filter(F.col("event_time").startswith("2026-08-15")).groupBy().count())
        chrono("Événements du 15 août, Parquet", pq.filter(F.col("jour") == "2026-08-15").groupBy().count())

    # ---------------------------------------------------------------- partie 4
    if mode == "taches":
        ev = enrichir(lire(spark, chemin))
        depuis = nombre_jobs(spark)
        chrono("Top des marques", ev.filter((F.col("event_type") == "purchase") & F.col("brand").isNotNull())
                                    .groupBy("brand").count().orderBy(F.desc("count")).limit(10), 3)
        stages(spark, depuis)
        depuis = nombre_jobs(spark)
        chrono("Clients distincts par jour", ev.groupBy("jour").agg(F.countDistinct("user_id").alias("clients")), 3)
        stages(spark, depuis)
    if mode == "cache":
        achats = enrichir(lire(spark, chemin)).filter(F.col("event_type") == "purchase").cache()
        chrono("Remplir le cache", achats.groupBy().count())
        chrono("Marques", achats.groupBy("brand").count(), 3)
        chrono("Rayons", achats.groupBy("rayon").agg(F.round(F.sum("prix")).cast("long").alias("chiffre")), 3)
        chrono("Jours", achats.groupBy("jour").count(), 3)
        print("Niveau de stockage :", achats.storageLevel)
        achats.unpersist(blocking=True)
    if mode == "aqe":
        pq = spark.read.parquet(PARQUET_HDFS if chemin.startswith("hdfs:") else PARQUET)
        spark.conf.set("spark.sql.shuffle.partitions", "200")
        for aqe in ("false", "true"):
            spark.conf.set("spark.sql.adaptive.enabled", aqe)
            depuis = nombre_jobs(spark)
            debut = time.perf_counter()
            pq.groupBy("rayon").agg(F.sum("prix")).write.format("noop").mode("overwrite").save()
            print(f"AQE {aqe} : {time.perf_counter() - debut:.1f} s")
            stages(spark, depuis)
    if mode == "fenetre":
        from pyspark.sql import Window
        pq = spark.read.parquet(PARQUET_HDFS if chemin.startswith("hdfs:") else PARQUET)
        w = Window.partitionBy("rayon").orderBy(F.desc("achats"), "product_id")
        top3 = (pq.filter((F.col("event_type") == "purchase") & F.col("rayon").isNotNull())
                  .groupBy("rayon", "product_id", "brand").agg(F.count("*").alias("achats"))
                  .withColumn("rang", F.row_number().over(w)).filter(F.col("rang") <= 3).orderBy("rayon", "rang"))
        plan = top3._jdf.queryExecution().executedPlan().toString()
        print("Exchange dans le plan :", plan.count("Exchange"))
        chrono("Top 3 de chaque rayon", top3, 30)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=["verifier", "lire", "rdd", "paresseux", "plan", "interface",
                                         "colonnes", "agreger", "duel", "cinq", "sql", "jointure",
                                         "rapport", "parquet", "taches", "cache", "aqe", "fenetre", "tout"])
    parser.add_argument("--entree", help="URI d'un CSV visible depuis tous les executors")
    parser.add_argument("--local", action="store_true", help="une machine, deux threads de travail")
    parser.add_argument("--attendre", type=int, default=0,
                        help="secondes pour consulter l'interface 4040 avant de fermer la session")
    args = parser.parse_args()
    par_defaut = AOUT_CSV if args.mode in ("duel", "cinq", "rapport", "parquet", "taches", "cache", "aqe", "fenetre") else PETIT_CSV
    spark = creer_session(local=args.local)
    try:
        demontrer(spark, args.mode, args.entree or par_defaut)
        if args.attendre > 0:
            print(f"Interface ouverte {args.attendre} s : http://localhost:4040", flush=True)
            time.sleep(args.attendre)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
