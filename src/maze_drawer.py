import pygame

from .drawer import Frame
from .parsing import Config
from .maze import get_maze


"""
class Config(BaseModel):
    highscore_filename: str
    width_and_height: list[list[int]]
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int = Field(gt=0)
    points_per_super_pacgum: int = Field(gt=0)
    points_per_ghost: int = Field(gt=0)
    seeds: list[int]
    level_max_time: int = Field(gt=0)
"""


class MazeDrawer(Frame):
    def __init__(self, size: tuple[int, int], config: Config) -> None:
        self.surface = pygame.Surface(size)
        self.size = size
        self.config = config

        self.generator = get_maze(self.config)
        self.maze = next(self.generator)

        self.maze_height, self.maze_width = (len(self.maze[0]), len(self.maze))
        self.wall_width = 3
        self.cell_size = (
            min(self.size) //
            min(self.maze_height, self.maze_width)
        )

        self.wall_color = (255, 255, 180)

    def draw_maze(self) -> None:
        """
        Render the full maze grid, including start and end cells.
        """

        self.fill((255, 180, 255))

        for y in range(self.maze_height):
            for x in range(self.maze_width):
                self.draw_cell(
                    self.maze[y][x], (x, y)
                )

    def draw_cell(self, value: int, cell: tuple[int, int]) -> None:
        x, y = cell

        px = x * self.cell_size + 0
        py = y * self.cell_size + 0

        x1, y1 = px, py
        x2, y2 = px + self.cell_size, py + self.cell_size

        if value == 15:
            self.draw_rect(
                (x1, y1),
                (x2, y2),
                (0, 0, 0)
            )
            return

        if value & 1:
            self.draw_rect(
                (x1, y1),
                (x2, y1 + self.wall_width),
                (255, 0, 0)
            )

        if value & 2:
            self.draw_rect(
                (x2 - self.wall_width, y1),
                (x2, y2),
                (0, 255, 0)
            )

        if value & 4:
            self.draw_rect(
                (x1, y2 - self.wall_width),
                (x2, y2),
                (0, 0, 255)
            )

        if value & 8:
            self.draw_rect(
                (x1, y1),
                (x1 + self.wall_width, y2),
                (255, 255, 0)
            )

    def draw_gum(self) -> None:
        pass
