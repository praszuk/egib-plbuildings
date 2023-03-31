.ONESHELL:
.PHONY: install test run clean

VENV=.venv
PYTHON=$(VENV)/bin/python3

install:
	virtualenv -p python3 $(VENV)
	source $(VENV)/bin/activate
	$(PYTHON) -m pip install -r requirements.txt

test:
	PYTHONPATH=backend $(PYTHON) -m pytest

run:
	cd backend
	$(PYTHON) -m uvicorn main:app --reload

clean:
	rm -rf .pytest_cache __pycache__ $(VENV)