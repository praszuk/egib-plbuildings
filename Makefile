.PHONY: install test mypy black black-check isort isort-check format format-check run clean

SHELL := /bin/bash
VENV=.venv
PYTHON=$(VENV)/bin/python3
APP_DIR=backend

install:
	virtualenv -p python3 $(VENV)
	source $(VENV)/bin/activate
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest $(ARGS) $(APP_DIR)

mypy:
	$(PYTHON) -m mypy --install-types --non-interactive $(APP_DIR)

isort:
	$(PYTHON) -m isort $(APP_DIR)

isort-check:
	$(PYTHON) -m isort --check $(APP_DIR)

black-check:
	$(PYTHON) -m black --check --diff $(APP_DIR)

black:
	$(PYTHON) -m black $(APP_DIR)

format: isort black

format-check: isort-check black-check

run:
	$(PYTHON) -m uvicorn $(APP_DIR).main:app --reload

clean:
	rm -rf .pytest_cache .mypy_cache __pycache__ $(VENV)