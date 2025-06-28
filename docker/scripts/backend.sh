#!/bin/bash

: "${DJANGO_SETTINGS_MODULE:=config.settings.local}"
: "${ENVIRONMENT:=LOCAL}"

export DJANGO_SETTINGS_MODULE
export ENVIRONMENT

echo "Environment: $ENVIRONMENT"
echo "Django Settings Module: $DJANGO_SETTINGS_MODULE"

echo "Making and applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting the server..."
if [ "$ENVIRONMENT" = "LOCAL" ]; then
    echo "Running Django development server..."
    exec python manage.py runserver 0.0.0.0:8000
elif [ "$ENVIRONMENT" = "PRODUCTION" ]; then
    echo "Running Gunicorn server..."
    exec gunicorn --bind 0.0.0.0:8000 --timeout 200 --threads=3 --worker-connections=1000 config.wsgi:application
else
    echo "Error: ENVIRONMENT must be either 'LOCAL' or 'PRODUCTION'. Got: $ENVIRONMENT"
    exit 1
fi