#!/bin/bash

# Exit script on error
set -e

echo "Waiting for MySQL..."
wait-for-mysql.sh

echo "Running makemigrations..."
python manage.py makemigrations
echo "Running migrations..."
python manage.py migrate

echo "Starting application..."
exec gunicorn --bind 0.0.0.0:8000 UserList.wsgi