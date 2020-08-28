#!/bin/sh
sleep 2  # let the DB wake up
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py shell < prefill.py