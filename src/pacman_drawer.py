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
        super().__init__(size, config)

        self.ghosts_img_copy = {
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

        self.ghosts_img = self.ghosts_img_copy.copy()

        self.pacman_img_copy = pygame.image.load(
            "assets/pacman/pacman.png").convert_alpha()

        PacManDrawer.update_size(self, size)

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

    def update_size(self, new_size):
        super().update_size(new_size)

        for image in self.ghosts_img:
            self.ghosts_img[image] = pygame.transform.scale(
                self.ghosts_img_copy[image], (self.cell_size, self.cell_size)
            )

        self.pacman_img = pygame.transform.scale(
                self.pacman_img_copy, (self.cell_size, self.cell_size)
            )
