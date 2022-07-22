#!/bin/sh

until cd /usr/src/scooter-kg
do
    echo "Waiting for server volume..."
done

until ./manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

./manage.py collectstatic --noinput
./manage.py runserver 0.0.0.0:8000