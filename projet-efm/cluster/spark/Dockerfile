# Image commune à Jupyter (le driver) et aux workers Spark.
# Les exécuteurs doivent avoir exactement la même version de Python et les mêmes
# bibliothèques que le driver : on construit donc une seule image pour les deux.
ARG IMAGE_JUPYTER=quay.io/jupyter/pyspark-notebook:2026-10-19
FROM ${IMAGE_JUPYTER}

# Clients Python des bases et de Kafka, utilisés depuis le driver et dans les
# fonctions foreachPartition / foreachBatch exécutées par les workers.
RUN pip install --no-cache-dir pymongo redis cassandra-driver neo4j kafka-python

# Connecteur Kafka de Spark, téléchargé une fois ici : la démonstration ne dépend
# pas d'internet. On ne copie que les jars propres au connecteur, pour ne pas
# dupliquer ceux que Spark fournit déjà.
RUN echo 'pass' > /tmp/vide.py \
 && spark-submit --master 'local[1]' --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0 /tmp/vide.py \
 && mkdir -p /tmp/jars-kafka \
 && find /home/${NB_USER} -path '*ivy*' -name '*.jar' \( -name 'spark-sql-kafka*' -o -name 'spark-token-provider-kafka*' -o -name 'kafka-clients*' -o -name 'commons-pool2*' \) -exec cp {} /tmp/jars-kafka/ \; \
 && ls /tmp/jars-kafka

USER root
RUN for jar in /tmp/jars-kafka/*.jar; do \
      nom=$(basename "$jar" | sed 's/-[0-9][0-9.]*\.jar$//'); \
      ls /usr/local/spark/jars | grep -q "^${nom}-[0-9]" || cp "$jar" /usr/local/spark/jars/; \
    done \
 && rm -rf /tmp/jars-kafka
COPY spark-defaults.conf /usr/local/spark/conf/spark-defaults.conf
USER ${NB_UID}
