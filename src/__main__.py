"""Entry point for the Pac-Man game application."""

import os
import sys
from pathlib import Path
from sys import argv

from src.monitor import Monitor
from src.errors import ParsingError


def _prepare_bundle() -> None:
    """Set the bundle working directory and default configuration."""
    if getattr(sys, "frozen", False):
        os.chdir(Path(sys.executable).resolve().parent)
        if len(sys.argv) == 1:
            sys.argv.append("assets/default_config.jsonc")


def main() -> None:
    """Run the game using the JSON config file passed as argument."""
    try:
        if len(argv) != 2:
            raise ParsingError("It must take exactly one argument.")

        Monitor(argv[1]).main_loop()

    except (PacmanError, ValidationError, KeyboardInterrupt, Exception) as e:
        print(f"[ERROR]: {e}")


if __name__ == "__main__":
    _prepare_bundle()
    try:
        main()
    except (BaseException) as e:
        print(f"[ERROR]: {e}")
