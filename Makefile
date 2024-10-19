# Makefile for managing Docker commands

# Variables
DOCKER_COMPOSE=docker-compose
SERVICE=blogapp

# Commands
build:
	$(DOCKER_COMPOSE) up --build -d

up:
	$(DOCKER_COMPOSE) up -d

ssh:
	$(DOCKER_COMPOSE) exec $(SERVICE) bash

server:
	$(DOCKER_COMPOSE) exec $(SERVICE) python manage.py runserver 0.0.0.0:8000

down:
	$(DOCKER_COMPOSE) down

flake8:
	$(DOCKER_COMPOSE) exec $(SERVICE) flake8 .

test:
	$(DOCKER_COMPOSE) exec $(SERVICE) python -m unittest discover  # or whatever command to run your tests
