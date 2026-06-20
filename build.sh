#!/usr/bin/env bash
# Render build script — runs on every deploy.
# Exit immediately if any command fails.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate
