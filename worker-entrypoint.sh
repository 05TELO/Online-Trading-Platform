#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done

echo "Run celery"
poetry run celery -A project worker --loglevel=info -B