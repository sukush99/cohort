run:
	uv run run.py

lint:
	ruff check --fix

format:
	ruff format .