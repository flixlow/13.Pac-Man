LINT_FLAG := --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

install: Makefile
	uv sync
	@echo "\033[0;32m\n[OK] installation completed ✔\n\033[0m"

run:
	uv run -m src config.json

debug:
	uv run -m pdb -m src

clean:
	rm -rf .venv

lint:
	uv run -m flake8 src && uv run -m mypy $(LINT_FLAG) src

lint-strict:
	uv run -m flake8 src && uv run -m mypy --strict

.PHONY: install run debug clean lint lint-strict