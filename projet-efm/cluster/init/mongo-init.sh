#!/bin/bash
# Assemble le cluster MongoDB shardé : un serveur de configuration, deux shards,
# un routeur mongos. Le script peut être relancé : il ne refait que ce qui manque.
set -e

attendre() {
  until mongosh --quiet --host "$1" --eval 'db.adminCommand({ping: 1}).ok' >/dev/null 2>&1; do
    sleep 2
  done
}

initier() {   # $1 = hôte:port, $2 = nom du replica set, $3 = options en plus
  mongosh --quiet --host "$1" --eval "
    try { rs.status(); print('$2 déjà initialisé'); }
    catch (e) { rs.initiate({_id: '$2', $3 members: [{_id: 0, host: '$1'}]}); print('$2 initialisé'); }"
}

attendre mongo-config:27019
initier mongo-config:27019 cfg "configsvr: true,"

for n in 1 2; do
  attendre "mongo-shard$n:27018"
  initier "mongo-shard$n:27018" "shard$n"
done

attendre mongo-router:27017
for n in 1 2; do
  until mongosh --quiet --host mongo-router:27017 --eval "
      if (db.getSiblingDB('config').shards.countDocuments({_id: 'shard$n'}) === 0) {
        sh.addShard('shard$n/mongo-shard$n:27018');
      }
      quit(db.getSiblingDB('config').shards.countDocuments({_id: 'shard$n'}) === 1 ? 0 : 1);" >/dev/null 2>&1; do
    sleep 3
  done
  echo "shard$n ajouté au cluster"
done

echo "Cluster MongoDB prêt : connectez-vous au routeur mongo-router:27017."
