import pygame

from maze_drawer import MazeDrawer
from parsing import Config


class PacManDrawer(MazeDrawer):
    def __init__(self, size: tuple[int, int], config: Config) -> None:
        self.surface = pygame.Surface(size)
        self.size = size
        self.config = config

        # self.generator = get_maze(self.config)
        self.maze = next(self.generator)

        self.maze_height, self.maze_width = (len(self.maze[0]), len(self.maze))
        self.wall_width = 3
        self.cell_size = (
            min(self.size) //
            min(self.maze_height, self.maze_width)
        )

        self.wall_color = (255, 255, 180)

# PAS FINI NE PAS REGARDER