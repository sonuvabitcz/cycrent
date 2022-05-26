#!/bin/sh

while ! nc -z db 3306 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done

# Removes all data from the database
# python manage.py flush --no-input
# python manage.py makemigrations --no-input
# python manage.py migrate

python manage.py runserver 0.0.0.0:8000