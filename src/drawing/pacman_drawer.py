import pygame

from .maze_drawer import MazeDrawer
from ..utils import GhostColor
from ..maze import MazeLevel


class PacManDrawer(MazeDrawer):
    def __init__(self, size: tuple[int, int], maze: MazeLevel) -> None:
        super().__init__(size, maze)

        self.ghosts_img_copy = {
            GhostColor.RED: pygame.image.load(
                "assets/ghosts/red_ghost.png").convert_alpha(),
            GhostColor.BLUE: pygame.image.load(
                "assets/ghosts/blue_ghost.png").convert_alpha(),
            GhostColor.ORANGE: pygame.image.load(
                "assets/ghosts/orange_ghost.png").convert_alpha(),
            GhostColor.GREEN: pygame.image.load(
                "assets/ghosts/green_ghost.png").convert_alpha(),
            GhostColor.SECRET: pygame.image.load(
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

        gum = (5, (255, 255, 210)) if not super else (7, (255, 60, 180))
        xc, yc = (x1 + x2) // 2, (y1 + y2) // 2

        self.draw_rect(
            (xc - gum[0] // 2, yc - gum[0] // 2),
            (xc + gum[0] // 2, yc + gum[0] // 2),
            gum[1]
        )

    def draw_ghost(self, cell: tuple[float, float], color: GhostColor) -> None:
        x, y = cell

        px = int(x * self.cell_size + self.offset_x)
        py = int(y * self.cell_size + self.offset_y)

        x1, y1 = px, py

        self.put_image((x1, y1), self.ghosts_img[color])

    def draw_pacman(self, cell: tuple[float, float]) -> None:
        x, y = cell

        px = int(x * self.cell_size + self.offset_x)
        py = int(y * self.cell_size + self.offset_y)

        x1, y1 = px, py

        self.put_image((x1, y1), self.pacman_img)

    def update_size(self, new_size: tuple[int, int]) -> None:
        super().update_size(new_size)

        for image in self.ghosts_img:
            self.ghosts_img[image] = pygame.transform.scale(
                self.ghosts_img_copy[image], (self.cell_size, self.cell_size)
            )

        self.pacman_img = pygame.transform.scale(
                self.pacman_img_copy, (self.cell_size, self.cell_size)
            )
