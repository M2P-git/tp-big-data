#!/bin/bash
# Assemble un Redis Cluster de six nœuds : trois principaux, chacun avec une réplique.
# Le script peut être relancé : il ne fait rien si le cluster existe déjà.
set -e

for n in 1 2 3 4 5 6; do
  until redis-cli -h "redis$n" ping 2>/dev/null | grep -q PONG; do sleep 1; done
done

if redis-cli -h redis1 cluster info | grep -q 'cluster_state:ok'; then
  echo "Redis Cluster déjà assemblé."
  exit 0
fi

noeuds=""
for n in 1 2 3 4 5 6; do
  noeuds="$noeuds $(getent hosts "redis$n" | awk '{print $1}'):6379"
done
redis-cli --cluster create $noeuds --cluster-replicas 1 --cluster-yes

until redis-cli -h redis1 cluster info | grep -q 'cluster_state:ok'; do sleep 1; done
echo "Redis Cluster prêt : 3 nœuds principaux, 3 répliques."
