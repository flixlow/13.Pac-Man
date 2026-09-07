from mazegenerator import MazeGenerator  # type: ignore

from .errors import GenerationError


def get_maze(size: tuple[int, int], seed: str) -> list[int]:
    try:
        generator = MazeGenerator(size, seed)
        generator.generate()
        return generator.maze
    except BaseException:
        raise GenerationError("Error occurs during maze generation.")


if __name__ == "__main__":
    print(get_maze((20, 20), "42"))
