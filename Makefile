.PHONY: build run clean rebuild migrate makemigrations test test-app test-app-class createapp

build:
	docker-compose build

run:
	docker-compose up

up:
	docker-compose up -d --build

up-logs:
	docker-compose up --build

down:
	docker-compose down

clean:
	docker-compose down --rmi all

rebuild: clean build

migrate:
	docker-compose exec app python manage.py migrate

makemigrations:
	docker-compose exec app python manage.py makemigrations

test:
	docker-compose exec app python manage.py test

test-app:
	docker-compose exec app python manage.py test $(app_name)

test-app-class:
	docker-compose exec app python manage.py test $(app_name).tests.$(class_name)

createapp:
	docker-compose exec app python manage.py startapp $(app_name)

createsuperuser:
	docker-compose exec app python manage.py createsuperuser
