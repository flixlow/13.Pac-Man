import pygame

from .maze_drawer import MazeDrawer
from ..utils import GhostColor, Parameters
from ..engine.maze import Maze
from ..engine.entity import Ghost, Entity, Direction


class PacManDrawer(MazeDrawer):
    def __init__(self, size: tuple[int, int], maze: Maze) -> None:
        super().__init__(size, maze)

        # self.ghosts_img_copy = {
        #     GhostColor.RED: pygame.image.load(
        #         "assets/ghosts/red/1.png").convert_alpha(),
        #     GhostColor.BLUE: pygame.image.load(
        #         "assets/ghosts/blue/1.png").convert_alpha(),
        #     GhostColor.ORANGE: pygame.image.load(
        #         "assets/ghosts/orange/1.png").convert_alpha(),
        #     GhostColor.GREEN: pygame.image.load(
        #         "assets/ghosts/pink/1.png").convert_alpha(),
        #     GhostColor.SECRET: pygame.image.load(
        #         "assets/ghosts/crazyman/3.png").convert_alpha()
        # }

        self.ghosts_img_copy = {
            GhostColor.RED: [pygame.image.load(
                f"assets/ghosts/red/{i+1}.png").convert_alpha() for i in range(8)],
            GhostColor.BLUE: [pygame.image.load(
                f"assets/ghosts/blue/{i+1}.png").convert_alpha() for i in range(8)],
            GhostColor.ORANGE: [pygame.image.load(
                f"assets/ghosts/orange/{i+1}.png").convert_alpha() for i in range(8)],
            GhostColor.PINK: [pygame.image.load(
                f"assets/ghosts/pink/{i+1}.png").convert_alpha() for i in range(8)],
            GhostColor.SECRET: [pygame.image.load(
                f"assets/ghosts/red/{i+1}.png").convert_alpha() for i in range(8)]
        }

        self.velocity = Parameters.PLAYER_VELOCITY
        self.movement_interval_ms: int = max(1, 1000 // self.velocity)
        self.player_move_elapsed_ms: int = 0
        self.animation_elapsed_ms: int = 0

        self.ghosts_img = self.ghosts_img_copy.copy()

        self.pacman_img_copy = pygame.image.load(
            "assets/pacman/pacman_1.png").convert_alpha()

        PacManDrawer.update_size(self, size)

    def draw_pacgum(self, cell: tuple[int, int], super: bool) -> None:
        x, y = cell

        px = x * self.cell_size + self.offset_x
        py = y * self.cell_size + self.offset_y

        x1, y1 = px, py
        x2, y2 = px + self.cell_size, py + self.cell_size

        gum = (
            (self.cell_size // 10, (255, 255, 210)) if not super else
            (self.cell_size // 5, (255, 60, 180))
        )
        xc, yc = (x1 + x2) // 2, (y1 + y2) // 2

        self.draw_rect(
            (xc - gum[0] // 2, yc - gum[0] // 2),
            (xc + gum[0] // 2, yc + gum[0] // 2),
            gum[1]
        )

    def draw_multiple_pacgums(
            self, cells: set[tuple[int, int]],
            super: bool = False) -> None:
        for cell in cells:
            self.draw_pacgum(cell, super=super)

    def display_entities(self, elapsed_t: int, entities: list[Entity]) -> None:
        for e in entities:
            e.animation_elapsed_ms = min(
                e.animation_elapsed_ms + elapsed_t,
                e.movement_interval_ms,
            )

            direction = e.get_direction()

            if isinstance(e, Ghost):
                params = (PacManDrawer.render_coords(elapsed_t, e), e.color)
                self.draw_ghost(*params, direction)
            else:
                self.draw_pacman(PacManDrawer.render_coords(elapsed_t, e))

    def update_animation(self, elapsed_ms: int) -> None:
        self.animation_elapsed_ms = min(
            self.animation_elapsed_ms + elapsed_ms,
            self.movement_interval_ms,
        )

    def draw_ghost(self, cell: tuple[float, float],
                   color: GhostColor, direction: Direction) -> None:
        x, y = cell

        px = int(x * self.cell_size + self.offset_x)
        py = int(y * self.cell_size + self.offset_y)

        x1, y1 = px, py

        match direction:
            case Direction.SOUTH:
                img = self.ghosts_img[color][0]
            case Direction.NORTH:
                img = self.ghosts_img[color][1]
            case Direction.WEST:
                img = self.ghosts_img[color][4]
            case Direction.EAST:
                img = self.ghosts_img[color][5]
            case _:
                img = self.ghosts_img[color][0]


        self.put_image((x1, y1), img)

    def draw_pacman(self, cell: tuple[float, float]) -> None:
        x, y = cell

        px = int(x * self.cell_size + self.offset_x + 0.1 * self.cell_size)
        py = int(y * self.cell_size + self.offset_y + 0.1 * self.cell_size)

        x1, y1 = px, py

        self.put_image((x1, y1), self.pacman_img)

    def update_size(self, new_size: tuple[int, int]) -> None:
        super().update_size(new_size)

        for color, images in self.ghosts_img.items():
            lst = []
            for image in images:
                scaled = pygame.transform.scale(
                    image, (self.cell_size, self.cell_size)
                )
                lst.append(scaled)
            self.ghosts_img[color] = lst

        self.pacman_img = pygame.transform.scale(
                self.pacman_img_copy, (
                    self.cell_size * 0.8, self.cell_size * 0.8)
            )

    @staticmethod
    def render_coords(elapsed: int, entity: Entity) -> tuple[float, float]:
        animation_progress = getattr(entity, "animation_elapsed_ms", elapsed)
        progress = min(
            animation_progress / max(1, entity.movement_interval_ms),
            1.0,
        )
        start_x, start_y = entity.previous_coords
        end_x, end_y = entity.coords
        return (
            start_x + (end_x - start_x) * progress,
            start_y + (end_y - start_y) * progress,
        )
