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
echo "Hello after collectstatic!!!"
python manage.py migrate
echo "Hello after migrate!!!"
# python manage.py createsuperuser
# echo "Hello after createsuperuser!!!"

uwsgi --socket :9000 --workers 4 --master --enable-threads --module cycrent.wsgi