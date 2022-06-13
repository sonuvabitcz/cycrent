#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web
ls -la /vol/web/static/
ls /vol/web/static/

whoami

while ! nc -z db 3306 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done

echo "Hello from run.sh!!!"

python manage.py collectstatic --noinput
python manage.py migrate


# gunicorn cycrent.wsgi:application --bind 0.0.0.0:8000
uwsgi --socket :9000 --workers 4 --master --enable-threads --module cycrent.wsgi