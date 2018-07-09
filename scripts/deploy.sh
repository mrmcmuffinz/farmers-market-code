#!/bin/sh

export NS=farmers-market-123

# create storage for mongodb.
kubectl create -f mongo/pv.yaml

# Create farmers customer namespace.
kubectl create namespace "$NS"

# Create MongoDB Stack.
kubectl -n "$NS" create -f mongo/pvc.yaml
kubectl -n "$NS" create -f mongo/secret.yaml
kubectl -n "$NS" create -f mongo/deployment.yaml
kubectl -n "$NS" create -f mongo/clusterip-svc.yaml

# TODO: Have some type of job to insert data into our mongodb.
sleep 10s

# Create Application Stack
kubectl -n "$NS" create -f farmers/configmap.yaml
kubectl -n "$NS" create -f farmers/deployment.yaml