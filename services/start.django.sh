#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

mkdir -p static

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --noinput

python manage.py shell -c "
from storage.models import User; 
import os;
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'test@gmail.com');
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '123451');
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
"

export GUNICORN_CMD_ARGS=${GUNICORN_CMD_ARGS:-" -b 0.0.0.0:8000 --timeout 30 --graceful-timeout 30 --forwarded-allow-ips=* --max-requests=10000 --chdir=/app"}
gunicorn api.wsgi:application