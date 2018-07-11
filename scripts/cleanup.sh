#!/bin/sh

export NS=farmers-market-123

# Cleanup Farmers App Stack
kubectl -n "$NS" delete -f farmers/deployment.yaml
kubectl -n "$NS" delete -f farmers/configmap.yaml

# Cleanup actual mongo db stack
kubectl -n "$NS" delete -f mongo/clusterip-svc.yaml
kubectl -n "$NS" delete -f mongo/deployment.yaml
kubectl -n "$NS" delete -f mongo/secret.yaml
kubectl -n "$NS" delete -f mongo/pvc.yaml

# Wait for prior resources to go away.
sleep 5s

# Cleanup mongodb data from pvc.
kubectl -n "$NS" create -f mongo/cleanup-job.yaml
# TODO: need to add logic to loop through cleanup job state.
sleep 10s
# Remove mongodb cleanup job.
kubectl -n "$NS" delete -f mongo/cleanup-job.yaml

kubectl delete ns "$NS"
kubectl delete -f mongo/pv.yaml