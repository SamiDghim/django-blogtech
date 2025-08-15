#!/bin/bash

docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d
sleep 5
docker-compose exec web npm install
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py seed_db
docker-compose exec web npm run build-once
