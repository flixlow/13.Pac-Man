LINT_FLAG := --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

install: Makefile mazegenerator-2.1.0-py3-none-any.whl
	uv sync
	@echo "\033[0;32m\n[OK] installation completed ✔\n\033[0m"

run:
	uv run -m src config.json

debug:
	uv run -m pdb -m src config.json

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf highscore.json
	rm -rf .venv
	uv clean

lint:
	uv run -m flake8 src && uv run -m mypy $(LINT_FLAG) src

lint-strict:
	uv run -m flake8 src && uv run -m mypy --strict src

.PHONY: install run debug clean lint lint-strict