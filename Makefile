create_db:
	sudo docker-compose exec database psql -U postgres -c "CREATE DATABASE film_library;"

migrate:
	python3 migrate.py db migrate

upgrade:
	python3 migrate.py db upgrade

downgrade:
	python3 migrate.py db downgrade

up_d:
	sudo docker compose up -d

up_build:
	sudo docker compose up --build

stop:
	sudo docker-compose down

rm:
	sudo docker rm -f $(sudo docker ps -a -q)

volume:
	sudo docker volume prune

network:
	sudo docker volume network

ps_a:
	sudo docker ps -a
