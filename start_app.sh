#!/bin/bash

cd "$(dirname "$0")"

POSTGRES_PASSWORD=$1
BUCKET=$2
KEY_ID=$3
SECRET_KEY=$4
DB_USER=$5
DB_PASS=$6

echo $POSTGRES_PASSWORD | docker secret create db_secret -

cd src && docker build --build-arg POSTGRES_PASSWORD=$POSTGRES_PASSWORD --build-arg BUCKET=$BUCKET --build-arg KEY_ID=$KEY_ID --build-arg SECRET_KEY=$SECRET_KEY --build-arg DB_USER=$DB_USER --build-arg DB_PASS=$DB_PASS -t photos-website .

docker volume create postgres_data

docker stack deploy -c docker-compose.yml photos-website
