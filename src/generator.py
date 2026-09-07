from mazegenerator import MazeGenerator  # type: ignore


def main() -> None:
    generator = MazeGenerator()
    generator.generate()
    print(generator.maze)
    print(generator)


if __name__ == "__main__":
    main()
