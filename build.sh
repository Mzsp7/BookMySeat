#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python scripts/add_seats.py
python scripts/setup_audit_accounts.py
python scripts/populate_movies.py
