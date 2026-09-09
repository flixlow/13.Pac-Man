import pygame

from .maze_drawer import MazeDrawer
from .parsing import Config

from enum import Enum, auto


class Ghost(Enum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    ORANGE = auto()
    SECRET = auto()


class PacManDrawer(MazeDrawer):
    def __init__(self, size: tuple[int, int], config: Config) -> None:
        self.surface = pygame.Surface(size)

        self.config = config

        self.maze = self.config.mazes[0]
        self.maze_height = len(self.maze)
        self.maze_width = len(self.maze[0])
        self.update_size(size)

        self.ghosts_img = {
            Ghost.RED: pygame.image.load(
                "assets/ghosts/red_ghost.png").convert_alpha(),
            Ghost.BLUE: pygame.image.load(
                "assets/ghosts/blue_ghost.png").convert_alpha(),
            Ghost.ORANGE: pygame.image.load(
                "assets/ghosts/orange_ghost.png").convert_alpha(),
            Ghost.GREEN: pygame.image.load(
                "assets/ghosts/green_ghost.png").convert_alpha(),
            Ghost.SECRET: pygame.image.load(
                "assets/ghosts/secret_ghost.png").convert_alpha()
        }

        self.pacman_img = pygame.image.load(
            "assets/pacman/pacman.png").convert_alpha()

        self.wall_color = (255, 255, 180)

    def draw_pacgum(self, cell: tuple[int, int], super: bool) -> None:
        x, y = cell

        px = x * self.cell_size + self.offset_x
        py = y * self.cell_size + self.offset_y

        x1, y1 = px, py
        x2, y2 = px + self.cell_size, py + self.cell_size

        gum = (3, (255, 255, 210)) if not super else (6, (255, 255, 255))
        self.draw_circle(
            ((x1 + x2) // 2, (y1 + y2) // 2), gum[0], color=gum[1]
        )

    def draw_ghost(self, cell: tuple[int, int], ghost_type: Ghost) -> None:
        x, y = cell

        px = x * self.cell_size + self.offset_x
        py = y * self.cell_size + self.offset_y

        x1, y1 = px, py

        self.put_image((x1, y1), self.ghosts_img[ghost_type])

    def draw_pacman(self, cell: tuple[int, int]) -> None:
        x, y = cell

        px = x * self.cell_size + self.offset_x
        py = y * self.cell_size + self.offset_y

        x1, y1 = px, py

        self.put_image((x1, y1), self.pacman_img)
