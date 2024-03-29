.PHONY: install run

install:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt && deactivate

run:
	. .venv/bin/activate && python pacman/run.py && deactivate

debug:
	. .venv/bin/activate && python -m pdb pacman/run.py && deactivate
