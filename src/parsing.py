from pydantic import BaseModel, Field
from pathlib import Path
import json
import sys

from errors import ParsingError


class Level(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)


class Config(BaseModel):
    highscore_filename: str
    levels: list[Level]
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int = Field(gt=0)
    points_per_super_pacgum: int = Field(gt=0)
    points_per_ghost: int = Field(gt=0)
    seed: str
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
        except OSError as e:
            raise ParsingError(e.__class__.__name__)
        except json.JSONDecodeError as e:
            raise ParsingError(
                f"Error occurs while reading {self.file.as_posix()}."
            ) from e
        return Config(**content)


if __name__ == "__main__":
    print(Parser(sys.argv[1]).open())
