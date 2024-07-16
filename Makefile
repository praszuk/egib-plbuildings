.PHONY: base-install install prod-install test mypy format format-check lint lint-check prod-run run clean healthcheck update

SHELL := /bin/bash
VENV=.venv
PYTHON=$(VENV)/bin/python
PROJECT_DIR=$(shell pwd)
APP_DIR=backend
LOG_CONFIG=$(APP_DIR)/core/log_config.yaml

base-install:
	virtualenv -p python3 $(VENV)
	source $(VENV)/bin/activate
	$(PYTHON) -m pip install GDAL==`gdal-config --version`
	$(PYTHON) -m pip install -r requirements/requirements.txt

install: base-install
	$(PYTHON) -m pip install -r requirements/requirements-dev.txt
	$(PYTHON) -m pip install -r requirements/requirements-test.txt
	if [ -d ".git" ]; then $(PYTHON) -m pre_commit install; fi

prod-install: base-install

test:
	$(PYTHON) -m pytest $(ARGS) $(APP_DIR)

mypy:
	$(PYTHON) -m mypy --install-types --non-interactive $(APP_DIR)

format:
	$(PYTHON) -m ruff format $(APP_DIR)

format-check:
	$(PYTHON) -m ruff format --diff $(APP_DIR)

lint:
	$(PYTHON) -m ruff check $(APP_DIR)

lint-check:
	$(PYTHON) -m ruff check --diff $(APP_DIR)

run:
	$(PYTHON) -m uvicorn $(APP_DIR).main:app --host 0.0.0.0 --reload --log-config $(LOG_CONFIG)

prod-run:
	$(PYTHON) -m uvicorn $(APP_DIR).main:app --host 0.0.0.0 --log-config $(LOG_CONFIG)

healthcheck:
	export PYTHONPATH=$(PROJECT_DIR) && \
	$(PYTHON) $(APP_DIR)/areas/healthcheck.py

clean:
	if [ -d ".git" ]; then $(PYTHON) -m pre_commit uninstall; fi
	rm -rf .pytest_cache .mypy_cache .counties_geoms.pickle __pycache__ $(VENV)

update:
	for filename in requirements/*.in; do pur -r $$filename; done
	pip-compile-multi