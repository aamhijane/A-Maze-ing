CONFIG_FILE: config.txt

install:
	.venv/bin/pip install requirements.txt

run:
	.venv/bin/python a_maze_ing.py $(CONFIG_FILE)

debug:
	.venv/bin/python -m pdb a_maze_ing.py $(CONFIG_FILE)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache

lint:
	.venv/bin/flake8 .
	.venv/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
