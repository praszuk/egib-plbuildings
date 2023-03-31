.ONESHELL:
.PHONY: install test

install:
	virtualenv -p python3 .venv
	source .venv/bin/activate
	pip install -r requirements.txt

test:
	PYTHONPATH=backend pytest
