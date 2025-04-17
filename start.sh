#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is up!"

# Run migrations and start the server
python manage.py migrate
python manage.py collectstatic --noinput
exec gunicorn backend_taxreminder.wsgi:application --bind 0.0.0.0:8000
