docker:
-  docker compose up
- docker-compose exec web bash
- docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser

reset database:
- docker-compose down
- docker volume rm studybuddy_postgres_data
- docker-compose exec web python manage.py migrate
- docker-compose exec web python manage.py createsuperuser

- docker-compose exec web python manage.py makemigrations
