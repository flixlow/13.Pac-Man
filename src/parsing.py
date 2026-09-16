from mazegenerator import MazeGenerator  # type: ignore
from pydantic import BaseModel, Field
from pathlib import Path
from random import seed, shuffle
import hashlib
import json
import sys

from .errors import GenerationError, ParsingError
from .maze import Maze


class LevelSize(BaseModel):
    width: int = Field(gt=6)
    height: int = Field(gt=6)


class Config(BaseModel):
    highscore_filename: str = Field(min_length=1)
    levels: list[LevelSize]
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int = Field(gt=0)
    points_per_super_pacgum: int = Field(gt=0)
    points_per_ghost: int = Field(gt=0)
    seed: int
    level_max_time: int = Field(gt=0)

    @staticmethod
    def _get_new_seed(seed: int) -> int:
        digest = hashlib.sha256(str(seed).encode()).digest()
        return int.from_bytes(digest, byteorder="big")

    @staticmethod
    def _get_corners(x_max: int, y_max: int) -> list[tuple[int, int]]:
        corners = [(0, 0), (x_max, 0), (0, y_max), (x_max, y_max)]
        seed()
        shuffle(corners)
        return corners

    def generate_all_maze(self) -> list[Maze]:
        mazes = []
        seed = self.seed

        for lvl in self.levels:
            try:
                g = MazeGenerator(size=(lvl.width, lvl.height), seed=seed)
                maze = Maze(
                    maze=g.maze, seed=seed, w=lvl.width, h=lvl.height,
                    corners=self._get_corners(lvl.width - 1, lvl.height - 1)
                )

                mazes.append(maze)
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
