import pygame

from .drawer import Frame
from .parsing import Config


class MazeDrawer(Frame):
    def __init__(self, size: tuple[int, int], config: Config) -> None:
        self.surface = pygame.Surface(size)

        self.maze_height = len(self.maze)
        self.maze_width = len(self.maze[0])
        self.update_size(size)

        self.wall_color = (255, 255, 180)

        self.draw_maze()

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

    def draw_cell(self, value: int, cell: tuple[int, int], bg: bool = False) -> None:
        x, y = cell

        px = x * self.cell_size + self.offset_x
        py = y * self.cell_size + self.offset_y

        x1, y1 = px, py
        x2, y2 = px + self.cell_size, py + self.cell_size

        if bg:
            self.draw_rect(
                (x1, y1),
                (x2, y2),
                (255, 180, 255)
            )

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

    def update_size(self, new_size: tuple[int, int]) -> None:
        super().update_size(new_size)

        self.cell_size = min(
            self.size[0] // self.maze_width,
            self.size[1] // self.maze_height
        )
        self.wall_width = 2 * max(1, (self.cell_size // 30))

        maze_width = self.maze_width * self.cell_size
        maze_height = self.maze_height * self.cell_size

        self.offset_x = (self.size[0] - maze_width) // 2
        self.offset_y = (self.size[1] - maze_height) // 2

        self.surface = pygame.Surface(new_size)
