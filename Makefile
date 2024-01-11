.PHONY: venv install run

venv:
	python -m venv .venv

install:
	pip install -r requirements.txt

run:
	. .venv/bin/activate && python pacman/run.py && deactivate
