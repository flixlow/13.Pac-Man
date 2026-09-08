import pygame

from .maze_drawer import MazeDrawer
from .parsing import Config


class PacManDrawer(MazeDrawer):
    def __init__(self, size: tuple[int, int], config: Config) -> None:
        self.surface = pygame.Surface(size)
        self.size = size
        self.config = config

        self.maze = self.config.mazes[0]

        self.maze_height, self.maze_width = (len(self.maze[0]), len(self.maze))
        self.wall_width = 3
        self.cell_size = (
            min(self.size) //
            min(self.maze_height, self.maze_width)
        )

        self.wall_color = (255, 255, 180)

    def draw_pacgum(self, cell: tuple[int, int], super: bool):
        radius = 3 if not super else 6
        x, y = cell

        px = x * self.cell_size + 0
        py = y * self.cell_size + 0

        x1, y1 = px, py
        x2, y2 = px + self.cell_size, py + self.cell_size

        self.draw_circle((x1 + x2 // 2, y1 + y2 // 2), radius)
