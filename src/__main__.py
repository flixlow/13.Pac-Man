from sys import argv
from pydantic import ValidationError

from .errors import ParsingError, PacmanError
from .engine.monitor import Monitor


def main() -> None:
    if len(argv) != 2:
        raise ParsingError(
            "It must take exactly one argument: a configuration file."
        )

    Monitor(argv[1]).main_loop()


if __name__ == "__main__":
    try:
        main()
    except (PacmanError, ValidationError, KeyboardInterrupt) as e:
        print(f"[ERROR]: {e}")
