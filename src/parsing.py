from mazegenerator import MazeGenerator
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Any
import hashlib
import json
import sys

from .errors import GenerationError
from .errors import ParsingError


class Level(BaseModel):
    width: int = Field(gt=10)
    height: int = Field(gt=10)


class Config(BaseModel):
    highscore_filename: str = Field(min_length=1)
    levels: list[Level]
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int = Field(gt=0)
    points_per_super_pacgum: int = Field(gt=0)
    points_per_ghost: int = Field(gt=0)
    seed: int
    level_max_time: int = Field(gt=0)
    mazes: list[list[list[int]]] = Field(default=[])

    def model_post_init(self, context: Any = None) -> None:
        self.mazes: list[list[list[int]]] = self._generate_all_maze()

    @staticmethod
    def _get_new_seed(seed: int) -> int:
        digest = hashlib.sha256(str(seed).encode()).digest()
        return int.from_bytes(digest, byteorder="big")

    def _generate_all_maze(self) -> list[list[list[int]]]:
        mazes = []
        seed = self.seed

        for level in self.levels:
            try:
                generator = MazeGenerator(
                    size=(level.width, level.height), seed=seed)
                mazes.append(generator.maze)
                seed = self._get_new_seed(seed)
            except BaseException:
                raise GenerationError("Error occurs during maze generation.")

        return mazes


def parsing(file_name: str) -> Config:
    file: Path = Path(file_name)
    if file.suffix != ".json":
        raise ParsingError("The config file must be a json.")
    try:
        with open(file, encoding="utf-8") as f:
            lines = [ln for ln in f if not ln.lstrip().startswith('#')]
            content = json.loads("".join(lines))
        return Config(**content)
    except OSError as e:
        raise ParsingError(f"{file_name}: {e.__class__.__name__}")
    except json.JSONDecodeError as e:
        raise ParsingError(
            f"Error occurs while reading {file.as_posix()}"
            f"(line {e.lineno})."
        ) from e


if __name__ == "__main__":
    print(parsing(sys.argv[1]))
