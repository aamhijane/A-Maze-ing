CONFIG_FILE = config.txt

ifdef VIRTUAL_ENV
    VENV      = $(VIRTUAL_ENV)
    VENV_NAME = $(notdir $(VENV))
    PYTHON    = $(VENV)/bin/python
    PIP       = $(VENV)/bin/pip
    FLAKE8    = $(VENV)/bin/flake8
    MYPY      = $(VENV)/bin/mypy
else
    VENV      =
    VENV_NAME =
    PYTHON    = python3
    PIP       = pip3
    FLAKE8    = flake8
    MYPY      = mypy
endif

LINT_FLAGS = --warn-return-any \
             --warn-unused-ignores \
             --ignore-missing-imports \
             --disallow-untyped-defs \
             --check-untyped-defs

venv:
	python3 -m venv .venv

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) a_maze_ing.py $(CONFIG_FILE)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG_FILE)

build:
	$(PYTHON) -m build --outdir .
	rm -rf mazegen.egg-info

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	rm -rf ./**/__pycache__ ./**/.mypy_cache ./**/.pytest_cache
	rm -rf mazegen.egg-info

lint:
	$(if $(VENV_NAME), $(FLAKE8) --exclude=$(VENV_NAME) ., $(FLAKE8) .)
	$(MYPY) . $(LINT_FLAGS)

lint_strict:
	$(if $(VENV_NAME), $(FLAKE8) --exclude=$(VENV_NAME) ., $(FLAKE8) .)
	$(MYPY) . --strict

.PHONY: venv install run debug build clean lint lint_strictcd
