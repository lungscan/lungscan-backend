.PHONY: help install run dev down restart

help:
	@echo "Commands:"
	@echo "install    : install dependencies"
	@echo "run        : run the application in production mode"
	@echo "dev        : run the application in development mode with docker"
	@echo "down       : stop the development docker containers"
	@echo "restart    : restart the development docker containers"

install:
	pip install -r requirements.txt

run:
	@set FLASK_ENV=production&& flask run

dev:
	@if not exist .env (copy .env.example .env)
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose down
	docker-compose up -d