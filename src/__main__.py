import sys
from pydantic import ValidationError

from .errors import ParsingError, PacmanError
from .monitor import Monitor


def main():
    if len(sys.argv) != 2:
        raise ParsingError(
            "It must take exactly one argument: a configuration file."
        )

    Monitor(sys.argv[1]).main_loop()


if __name__ == "__main__":
    try:
        main()
    except (PacmanError, ValidationError) as e:
        print(f"[ERROR]: {e}")
