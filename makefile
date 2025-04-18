.PHONY: install run clean distclean

ACTIVATE :=
ifeq ($(OS), Windows_NT)
	ACTIVATE += .venv/Scripts/activate
else
	ACTIVATE += .venv/bin/activate
endif

install:
	python -m venv .venv
	. $(ACTIVATE) && pip install -r requirements.txt && deactivate

run:
	. $(ACTIVATE) && python pacman/run.py && deactivate

debug:
	. $(ACTIVATE) && python -m pdb pacman/run.py && deactivate

clean:
	rm -rf pacman/__pycache__

distclean: $(clean)
	rm -rf .venv
