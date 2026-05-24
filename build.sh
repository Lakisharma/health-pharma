#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed database with initial data (setup superuser, categories, products, company info)
python manage.py setup
