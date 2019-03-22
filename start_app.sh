#!/bin/bash

cd "$(dirname "$0")"

BUCKET=$1
KEY_ID=$2
SECRET_KEY=$3
DB_USER=$4
DB_PASS=$5

cd src && docker build --build-arg BUCKET=$BUCKET --build-arg KEY_ID=$KEY_ID --build-arg SECRET_KEY=$SECRET_KEY --build-arg DB_USER=$DB_USER --build-arg DB_PASS=$DB_PASS -t photos-website .

docker volume create postgres_data

docker-compose up -d