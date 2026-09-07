from mazegenerator import MazeGenerator  # type: ignore


def get_maze(seed: str) -> list[int]:
    generator = MazeGenerator()
    generator.generate(seed)
    return generator.maze


if __name__ == "__main__":
    print(get_maze(42))
