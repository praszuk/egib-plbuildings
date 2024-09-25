.PHONY: install test format format-check lint lint-check clean healthcheck update drun dprod-run dclean

SHELL := /bin/bash
VENV=.venv
PYTHON=$(VENV)/bin/python
PROJECT_DIR=$(shell pwd)
APP_DIR=backend
LOG_CONFIG=$(APP_DIR)/core/log_config.yaml

install:
	virtualenv -p python3 $(VENV)
	source $(VENV)/bin/activate
	$(PYTHON) -m pip install GDAL==`gdal-config --version`
	$(PYTHON) -m pip install -r requirements/requirements.txt -r requirements/requirements-dev.txt -r requirements/requirements-test.txt
	if [ -d ".git" ]; then $(PYTHON) -m pre_commit install; fi

test:
	$(PYTHON) -m pytest $(ARGS) $(APP_DIR)

format:
	$(PYTHON) -m ruff format $(APP_DIR)

format-check:
	$(PYTHON) -m ruff format --diff $(APP_DIR)

lint:
	$(PYTHON) -m ruff check $(APP_DIR)

lint-check:
	$(PYTHON) -m ruff check --diff $(APP_DIR)

drun:
	docker compose -f docker-compose-dev.yml up

dprod-run:
	docker compose -f docker-compose-prod.yml up

dclean:
	docker compose -f docker-compose-dev.yml down
	docker compose -f docker-compose-prod.yml down

healthcheck:
	docker compose -f docker-compose-prod.yml exec backend bash -c "export PYTHONPATH=/app;python backend/areas/healthcheck.py"

clean:
	if [ -d ".git" ]; then $(PYTHON) -m pre_commit uninstall; fi
	rm -rf .pytest_cache .counties_geoms.pickle __pycache__ $(VENV)

update:
	for filename in requirements/*.in; do pur -r $$filename; done
	pip-compile-multi