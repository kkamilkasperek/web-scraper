#!/bin/bash


if [ -z "$DJANGO_SECRET_KEY" ]; then
    export DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
fi

# Uruchom migracje i Gunicorn
python manage.py migrate
exec gunicorn web_scraper.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120