"""Utilities for parsing and validating the game configuration.

This module loads JSON configuration files, validates the structure of the
game settings and generates the mazes for each configured level.
"""

from pathlib import Path
from hashlib import sha256
from random import seed, shuffle
from pydantic import BaseModel, Field
from json import loads, JSONDecodeError
from mazegenerator import MazeGenerator  # type: ignore

from .errors import GenerationError, ParsingError
from .engine.maze import Maze


class Points(BaseModel):
    """Point values awarded for collecting different items in the maze.

    Attributes:
        per_pacgum: Number of points awarded for each regular pacgum.
        per_super_pacgum: Number of points awarded for each super pacgum.
        per_ghost: Number of points awarded for each defeated ghost.
    """

    per_pacgum: int = Field(gt=0)
    per_super_pacgum: int = Field(gt=0)
    per_ghost: int = Field(gt=0)


class LevelSize(BaseModel):
    """Size of a single maze level.

    Attributes:
        width: Width of the level in tiles.
        height: Height of the level in tiles.
    """

    width: int = Field(gt=6)
    height: int = Field(gt=6)


class Config(BaseModel):
    """Configuration object for a game session.

    Attributes:
        highscore_filename: Name of the file used to store the high score.
        levels: List of sizes for each level.
        lives: Number of lives available to the player.
        points: Point values for all collectible items.
        seed: Initial random seed used for maze generation.
        level_max_time: Maximum allowed time for a level.
    """

    highscore_filename: str = Field(min_length=1)
    levels: list[LevelSize]
    lives: int = Field(gt=0)
    points: Points
    seed: int
    level_max_time: int = Field(gt=0)

    @staticmethod
    def _get_new_seed(seed: int) -> int:
        """Generate a new deterministic seed from a given seed value.

        Args:
            seed: The current seed used in the generation process.

        Returns:
            The next seed computed from the input value.
        """

        digest = sha256(str(seed).encode()).digest()
        return int.from_bytes(digest, byteorder="big")

    @staticmethod
    def _get_corners(x_max: int, y_max: int) -> list[tuple[int, int]]:
        """Return the four maze corners in a shuffled order.

        Args:
            x_max: Maximum x index of the maze.
            y_max: Maximum y index of the maze.

        Returns:
            A list containing the corner coordinates in randomized order.
        """

        corners = [(0, 0), (x_max, 0), (0, y_max), (x_max, y_max)]
        seed()
        shuffle(corners)
        return corners

    def generate_all_maze(self) -> list[Maze]:
        """Generate all mazes declared in the configuration.

        Returns:
            A list of generated maze objects, one per configured level.

        Raises:
            GenerationError: If maze generation fails for any level.
        """

        mazes = []
        seed = self.seed

        for lvl in self.levels:
            try:
                g = MazeGenerator(size=(lvl.width, lvl.height), seed=seed)
                maze = Maze(
                    maze_map=g.maze, seed=seed, w=lvl.width, h=lvl.height,
                    corners=self._get_corners(lvl.width - 1, lvl.height - 1)
                )

                mazes.append(maze)
                seed = self._get_new_seed(seed)
            except BaseException:
                raise GenerationError("Error occurs during maze generation.")

        return mazes


def parsing(file_name: str) -> Config:
    """Parse a JSON configuration file into a validated Config object.

    Args:
        file_name: Path to the configuration JSON file.

    Returns:
        The parsed and validated configuration.

    Raises:
        ParsingError: If the file does not use the JSON extension, cannot be
            opened, or contains invalid JSON content.
    """

    file: Path = Path(file_name)
    if file.suffix != ".json":
        raise ParsingError("The config file must be a json.")
    try:
        with open(file, encoding="utf-8") as f:
            lines = [ln for ln in f if not ln.lstrip().startswith('#')]
            content = loads("".join(lines))
        return Config(**content)
    except OSError as e:
        raise ParsingError(f"{file_name}: {e.__class__.__name__}")
    except JSONDecodeError as e:
        raise ParsingError(
            f"Error occurs while reading {file.as_posix()}"
            f"(line {e.lineno})."
        ) from e
