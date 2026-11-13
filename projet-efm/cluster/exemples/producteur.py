"""Rejouer un fichier CSV dans Kafka, à débit réglable.

Chaque ligne devient un message JSON, avec deux champs ajoutés :
- id : un identifiant stable (le numéro de ligne), pour repérer les doublons ;
- emis_a : l'instant d'émission en millisecondes, pour mesurer le délai de bout en bout.

    python /home/jovyan/exemples/producteur.py --fichier /home/jovyan/donnees/clickstream.csv \\
        --topic clics --debit 2000 --debut 0 --nombre 20000
"""
import argparse
import csv
import json
import time

from kafka import KafkaProducer

parser = argparse.ArgumentParser()
parser.add_argument("--fichier", required=True)
parser.add_argument("--topic", required=True)
parser.add_argument("--debit", type=int, default=1000, help="messages par seconde")
parser.add_argument("--debut", type=int, default=0, help="première ligne à envoyer")
parser.add_argument("--nombre", type=int, default=10000, help="nombre de lignes à envoyer")
parser.add_argument("--cle", default="user_id", help="colonne qui sert de clé Kafka")
args = parser.parse_args()

producteur = KafkaProducer(
    bootstrap_servers=["kafka1:9092", "kafka2:9092", "kafka3:9092"],
    value_serializer=lambda v: json.dumps(v).encode(),
    key_serializer=lambda k: k.encode(),
    acks="all",          # le message est confirmé quand ses copies sont écrites
)

envoyes = 0
depart = time.time()
with open(args.fichier, newline="") as f:
    for numero, ligne in enumerate(csv.DictReader(f)):
        if numero < args.debut:
            continue
        if envoyes >= args.nombre:
            break
        ligne["id"] = numero
        ligne["emis_a"] = int(time.time() * 1000)
        # Même clé, même partition : l'ordre des événements d'un client est garanti.
        producteur.send(args.topic, key=ligne[args.cle], value=ligne)
        envoyes += 1
        attente = depart + envoyes / args.debit - time.time()
        if attente > 0:
            time.sleep(attente)

producteur.flush()
print(f"{envoyes} messages envoyés en {time.time() - depart:.1f} s "
      f"(lignes {args.debut} à {args.debut + envoyes - 1})")
