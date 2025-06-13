#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

mkdir -p static
#python manage.py makemigrations
#python manage.py migrate --run-syncdb
python manage.py collectstatic --noinput

export GUNICORN_CMD_ARGS=${GUNICORN_CMD_ARGS:-" -b 0.0.0.0:8000 --timeout 30 --graceful-timeout 30 --forwarded-allow-ips=* --max-requests=10000 --chdir=/app"}
gunicorn api.wsgi:application
