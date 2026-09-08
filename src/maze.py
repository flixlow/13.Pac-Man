from mazegenerator import MazeGenerator
from typing import Generator
import hashlib

from .errors import GenerationError
from .parsing import Config


def get_next_seed(seed: str) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()


def get_maze(config: Config) -> Generator[list[list[int]]]:
    seed = config.seed
    for level in config.levels:
        try:
            generator = MazeGenerator((level.width, level.height), config.seed)
            generator.generate()
            yield generator.maze
            seed = get_next_seed(seed)
        except BaseException:
            raise GenerationError("Error occurs during maze generation.")


if __name__ == "__main__":
    pass
