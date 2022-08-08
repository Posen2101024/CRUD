#!/bin/bash
set -euo pipefail

echo SECRET_KEY=\"$(tr -dc 'A-Za-z0-9!#%&()*+,-./:;<=>?@[\]^_{|}~' </dev/urandom | head -c100)\" > /etc/django-secret-key.env

django-admin collectstatic
django-admin migrate

django-admin runserver 0.0.0.0:8000
