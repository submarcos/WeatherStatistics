#!/usr/bin/env bash

cd /opt/weather || exit

# Activate venv
. /opt/venv/bin/activate

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    echo "Waiting for postgres..."
    sleep 0.1
done
echo "PostgreSQL reached"

# exec
exec "$@"
