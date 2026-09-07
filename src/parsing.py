from pydantic import BaseModel, Field
from pathlib import Path
import json
import sys

from src.errors import ParsingError


class Level(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)


class Config(BaseModel):
    highscore_filename: str
    levels: list[Level]
    seeds: list[int]
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int = Field(gt=0)
    points_per_super_pacgum: int = Field(gt=0)
    points_per_ghost: int = Field(gt=0)
    level_max_time: int = Field(gt=0)


class Parser:
    def __init__(self, file_name: str) -> None:
        self.file: Path = Path(file_name)
        if self.file.suffix != ".json":
            raise ParsingError("The config file must be a json.")

    def open(self) -> Config:
        try:
            with open(self.file, encoding="utf-8") as f:
                lines = []
                for line in f:
                    if line.lstrip().startswith(('#', "//")):
                        continue
                    lines.append(line)
                content = json.loads("".join(lines))
        except (OSError, json.JSONDecodeError) as e:
            raise ParsingError(
                f"Error occurs while reading {self.file.as_posix()}."
            ) from e
        return Config(**content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ParsingError(
            "It must take exactly one argument: a configuration file."
        )
    parser = Parser(sys.argv[1])
    config = parser.open()
    print(config.highscore_filename)
