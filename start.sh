#!/usr/bin/env bash
# exit on error
set -o errexit

# Run migrations
python manage.py migrate

# Seed database with initial data (setup superuser, categories, products, company info)
python manage.py setup

# Start the web server using Gunicorn
gunicorn newproject.wsgi
