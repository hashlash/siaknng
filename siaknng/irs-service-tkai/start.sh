#!/bin/bash
# cd dekoruma_backend

# Setup
# python3 manage.py makemigrations
# python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

# Start Gunicorn processes
# Run application
echo Starting Gunicorn.
exec gunicorn irs.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3