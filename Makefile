create_db:
	sudo docker-compose exec database psql -U postgres -c "CREATE DATABASE film_library;"

init:
	flask db init

migrate:
	flask db migrate

upgrade:
	flask db upgrade

downgrade:
	flask db downgrade

up_d:
	sudo docker compose up -d

up_build:
	sudo docker compose up --build

stop:
	sudo docker-compose down

rm:
	sudo docker rm -f $(sudo docker ps -a -q)

del_volume:
	sudo docker volume prune

del_network:
	sudo docker network prune

ps_a:
	sudo docker ps -a

used_memory:
	sudo docker system df

del_images:
	sudo docker rmi $(sudo docker images -a -q)

del_cache:
	sudo docker builder prune

freeze:
	pip freeze > requirements.txt

logs_file:
	sudo docker exec -i -t flask cat error.log

run_tests:
	sudo docker exec -it flask pytest tests

test_db:
	sudo docker-compose exec test-database psql --username=postgres --dbname=film_library_test

run_pylint:
	pylint $(git ls-files '*.py')

seed:
	sudo docker exec -it flask flask seed_all
