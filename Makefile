.PHONY: base-install install prod-install test mypy black black-check isort isort-check format format-check prod-run run clean

SHELL := /bin/bash
VENV=.venv
PYTHON=$(VENV)/bin/python
APP_DIR=backend

base-install:
	virtualenv -p python3 $(VENV)
	source $(VENV)/bin/activate
	$(PYTHON) -m pip install GDAL==`gdal-config --version`
	$(PYTHON) -m pip install -r requirements.txt

install: base-install
	$(PYTHON) -m pip install -r requirements-dev.txt
	$(PYTHON) -m pip install -r requirements-test.txt
	if [ -d ".git" ]; then $(PYTHON) -m pre_commit install; fi

prod-install: base-install

test:
	$(PYTHON) -m pytest $(ARGS) $(APP_DIR)

mypy:
	$(PYTHON) -m mypy --install-types --non-interactive $(APP_DIR)

isort:
	$(PYTHON) -m isort $(APP_DIR)

isort-check:
	$(PYTHON) -m isort --check --diff $(APP_DIR)

black-check:
	$(PYTHON) -m black --check --diff $(APP_DIR)

black:
	$(PYTHON) -m black $(APP_DIR)

format: isort black

format-check: isort-check black-check

run:
	$(PYTHON) -m uvicorn $(APP_DIR).main:app --host 0.0.0.0 --reload

prod-run:
	$(PYTHON) -m uvicorn $(APP_DIR).main:app --host 0.0.0.0

clean:
	if [ -d ".git" ]; then $(PYTHON) -m pre_commit uninstall; fi
	rm -rf .pytest_cache .mypy_cache __pycache__ $(VENV)