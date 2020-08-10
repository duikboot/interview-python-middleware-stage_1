DOCKER = docker
DOCKER-COMPOSE = docker-compose
GUNICORN = gunicorn
PYTEST = pytest

run-devel:
	$(GUNICORN) api.app:app -b 0.0.0.0:8000 --reload --log-level debug --access-logfile=- -t 9999


run-docker:
	$(DOCKER-COMPOSE) up

test:
	$(PYTEST) --capture=no --verbose --doctest-modules
