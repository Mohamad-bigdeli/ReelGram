#!/bin/bash

: "${DJANGO_SETTINGS_MODULE:=config.settings.local}"
: "${ENVIRONMENT:=LOCAL}"

export DJANGO_SETTINGS_MODULE
export ENVIRONMENT

if [ $ENVIRONMENT = "PRODUCTION" ]; then
    LOGLEVEL="CRITICAL"
else
    LOGLEVEL="DEBUG"
fi

echo "Running celery worker..."
celery -A config worker --loglevel=$LOGLEVEL 
