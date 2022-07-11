#!/bin/sh

cd /root/flask-project/

git fetch --all
git pull

source python3-virtualenv/bin/activate

docker compose -f docker-compose.prod.yml down

docker compose -f docker-compose.prod.yml up -d --build
