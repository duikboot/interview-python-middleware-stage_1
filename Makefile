DOCKER = docker
DOCKER-COMPOSE = docker-compose
GUNICORN = gunicorn

run-devel:
	$(GUNICORN) api.app:app -b 0.0.0.0:8000 --reload --log-level debug --access-logfile=- -t 9999


run-docker:
	$(DOCKER-COMPOSE) up

test:
	pytest -s
