from pydantic import BaseModel, Field
from pathlib import Path
import json
import sys

from .errors import ParsingError


class Level(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)


class Config(BaseModel):
    highscore_filename: str = Field(min_length=1)
    levels: list[Level]
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int = Field(gt=0)
    points_per_super_pacgum: int = Field(gt=0)
    points_per_ghost: int = Field(gt=0)
    seed: str = Field(min_length=1)
    level_max_time: int = Field(gt=0)


class Parser:
    def __init__(self, file_name: str) -> None:
        self.file: Path = Path(file_name)
        if self.file.suffix != ".json":
            raise ParsingError("The config file must be a json.")

    def open(self) -> Config:
        try:
            with open(self.file, encoding="utf-8") as f:
                lines = [ln for ln in f if not ln.lstrip().startswith('#')]
                content = json.loads("".join(lines))
            return Config(**content)
        except OSError as e:
            raise ParsingError(f"{self.file}: {e.__class__.__name__}")
        except json.JSONDecodeError as e:
            raise ParsingError(
                f"Error occurs while reading {self.file.as_posix()}"
                f"(line {e.lineno})."
            ) from e


if __name__ == "__main__":
    print(Parser(sys.argv[1]).open())
