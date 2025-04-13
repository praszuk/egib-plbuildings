.PHONY: install format format-check lint lint-check clean update

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
	$(PYTHON) -m pip install -r $(APP_DIR)/requirements/requirements.txt -r $(APP_DIR)/requirements/requirements-dev.txt -r $(APP_DIR)/requirements/requirements-test.txt
	if [ -d ".git" ]; then $(PYTHON) -m pre_commit install; fi

format:
	$(PYTHON) -m ruff format $(APP_DIR)

format-check:
	$(PYTHON) -m ruff format --diff $(APP_DIR)

lint:
	$(PYTHON) -m ruff check $(APP_DIR)

lint-check:
	$(PYTHON) -m ruff check --diff $(APP_DIR)

clean:
	if [ -d ".git" ]; then $(PYTHON) -m pre_commit uninstall; fi
	rm -rf .pytest_cache .counties_geoms.pickle __pycache__ $(VENV)

update:
	for filename in $(APP_DIR)/requirements/*.in; do pur -r $$filename; done
	pip-compile-multi -d $(APP_DIR)/requirements/