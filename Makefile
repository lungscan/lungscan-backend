.PHONY: help install run dev

help:
	@echo "Commands:"
	@echo "install    : install dependencies"
	@echo "run        : run the application in production mode"
	@echo "dev        : run the application in development mode"

install:
	pip install -r requirements.txt

run:
	@set FLASK_ENV=production&& flask run

dev:
	@if not exist .env (copy .env.example .env)
	@flask run
