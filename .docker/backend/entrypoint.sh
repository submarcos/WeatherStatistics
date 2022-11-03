#!/usr/bin/env bash

cd /opt/weather || exit

# Activate venv
. /opt/venv/bin/activate

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done
echo "PostgreSQL started"

# exec
exec "$@"
