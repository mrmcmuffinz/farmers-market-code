#!/usr/bin/env bash
echo "Creating mongo users..."
mongo admin \
      --host localhost \
      -u "$MONGO_INITDB_ROOT_USERNAME" \
      -p "$MONGO_INITDB_ROOT_PASSWORD" \
      --eval "db.createUser({user: 'farmeruser1', pwd: 'farmeruser1', roles: [{role: 'readWrite', db: 'farmers'}]});"
echo "Mongo users created."