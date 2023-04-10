.PHONY: install test run clean

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

run:
	$(PYTHON) -m uvicorn $(APP_DIR).main:app --reload

clean:
	rm -rf .pytest_cache __pycache__ $(VENV)