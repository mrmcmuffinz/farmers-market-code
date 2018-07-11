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

export MONGO_POD=$(kubectl -n "$NS" get pod -l 'run==mongodb' -o jsonpath='{.items[*].metadata.name}')

# Add auth user to mongodb so cli can talk to mongodb.
kubectl -n "$NS" exec -it "$MONGO_POD" -- sh -c "mongo admin --host localhost -u \$MONGO_INITDB_ROOT_USERNAME -p \$MONGO_INITDB_ROOT_PASSWORD --eval \"db.createUser({user: 'farmeruser1', pwd: 'farmeruser1', roles: [{role: 'readWrite', db: 'farmers'}]});\""

# Create Application Stack
kubectl -n "$NS" create -f farmers/configmap.yaml
kubectl -n "$NS" create -f farmers/deployment.yaml

# Wait for farmers app to startup.
sleep 5s

# Get pod name for farmers app.
export CLI_POD=$(kubectl -n "$NS" get pod -l 'run==farmers-app' -o jsonpath='{.items[*].metadata.name}')

# Run pytest for against farmers app.
kubectl -n "$NS" exec -it "$CLI_POD" -- bash -c "python -m pytest -vx tests/"