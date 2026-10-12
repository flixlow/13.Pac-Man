"""Entry point for the Pac-Man game application."""

from sys import argv
from pydantic import ValidationError

from .errors import ParsingError, PacmanError
from .monitor import Monitor


def main() -> None:
    """Run the game using the JSON config file passed as argument."""
    if len(argv) != 2:
        Monitor("assets/default_config.json").main_loop()
        print(ParsingError("It must take exactly one argument."))
    else:
        Monitor(argv[1]).main_loop()


if __name__ == "__main__":
    try:
        main()
    except (PacmanError, ValidationError, KeyboardInterrupt) as e:
        print(f"[ERROR]: {e}")
