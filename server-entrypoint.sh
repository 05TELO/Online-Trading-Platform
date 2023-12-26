#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done


until poetry run python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

echo "Collect static files"
poetry run python manage.py collectstatic --noinput

echo "Database loaddata"
poetry run python manage.py loaddata users_modified.json

echo "Creating superuser"
poetry run python manage.py createsuperuser-ifnotexists

echo "Starting server"
poetry run gunicorn -b 0.0.0.0:8000 project.wsgi:application