.PHONY: all
all: format lint pytest

.PHONY: format
format:
	uv run ruff format .

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: pytest
pytest:
	uv run pytest

