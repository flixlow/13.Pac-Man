from errors import ParsingError
import sys
from pathlib import Path


class Config(BaseModel):
    highscore_filename : highscore.json
    level : array of multiple levels
    width , height : for each level
    lives : 3
    pacgum : 42
    points_per_pacgum : 10
    points_per_super_pacgum : 50
    points_per_ghost : 200
    seed : 42
    level_max_time : 90


class Parser:
    def __init__(self, file_name: str) -> None:
        self.file: Path = Path(file_name)
        if self.file.suffix != ".json":
            raise ParsingError("The config file must be a json.")
        


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ParsingError(
            "It must take exactly one argument: a configuration file."
        )
    parser = Parser(sys.argv[1])
