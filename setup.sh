#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py shell < prefill.py