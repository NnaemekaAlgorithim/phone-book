#!/bin/sh
set -e

# Wait for the database to be ready
until pg_isready -h db -p 5432 -U phonebookuser; do
  echo "Waiting for postgres..."
  sleep 2
done

# Run migrations
python3 manage.py migrate

# Start Gunicorn
exec gunicorn phone_book.phone_book.wsgi:application --bind 0.0.0.0:8000
