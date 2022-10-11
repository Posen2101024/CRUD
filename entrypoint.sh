#!/bin/bash
set -euo pipefail

echo SECRET_KEY=\"$(tr -dc 'A-Za-z0-9!#%&()*+,-./:;<=>?@[\]^_{|}~' </dev/urandom | head -c100)\" > /etc/django-secret-key.env

django-admin collectstatic
django-admin migrate

openssl req -x509 -newkey rsa:4096 -keyout /etc/nginx/key.pem -out /etc/nginx/cert.pem -sha256 -days 365 -nodes -subj "/C=TW"
nginx -t
service nginx start

uwsgi --ini /crud/uwsgi.ini
