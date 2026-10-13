LINT_FLAG := --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
CONFIG := assets/default_config.jsonc

install: Makefile mazegenerator-2.1.0-py3-none-any.whl
	uv sync
	@echo "\033[0;32m\n[OK] installation completed ✔\n\033[0m"

run:
	@PYGAME_HIDE_SUPPORT_PROMPT=1 uv run -m src $(CONFIG)

debug:
	uv run -m pdb -m src $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf "build" "dist"
	rm -rf .venv
	uv clean

lint:
	uv run -m flake8 src && uv run -m mypy $(LINT_FLAG) src

lint-strict:
	uv run -m flake8 src && uv run -m mypy --strict src

build: clean
	@test -f highscores.json || printf '{}\n' > highscores.json
	uv run --locked pyinstaller --noconfirm --clean "Pac-Man.spec"
	cd dist && zip -qr "Pac-Man.zip" Pac-Man
	rm -rf build

.PHONY: install run debug clean lint lint-strict build
