.ONESHELL:
.PHONY: install test run clean

install:
	virtualenv -p python3 .venv
	source .venv/bin/activate
	pip install -r requirements.txt

test:
	PYTHONPATH=backend pytest

run:
	cd backend
	uvicorn main:app --reload

clean:
	rm -rf .pytest_cache __pycache__ .venv