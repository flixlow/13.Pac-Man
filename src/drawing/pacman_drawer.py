
import pygame
from random import choice

from ..engine.maze import Maze
from ..entity import Ghost, Entity
from .maze_drawer import MazeDrawer
from ..color_utils import theme
from ..utils import GhostColor, Parameters, Direction, Timer


class PacManDrawer(MazeDrawer):
    def __init__(self, size: tuple[int, int], maze: Maze, t: Timer) -> None:
        super().__init__(size, maze)

        self.fruit_n = choice([0, 1, 2])
        self.timer = t
        self.last_pacman_direction: Direction = Direction.START

        self.ghosts_img_copy = {
            GhostColor.RED: [pygame.image.load(
                f"assets/ghosts/red/{i+1}.png").convert_alpha()
                for i in range(8)],
            GhostColor.BLUE: [pygame.image.load(
                f"assets/ghosts/blue/{i+1}.png").convert_alpha()
                for i in range(8)],
            GhostColor.ORANGE: [pygame.image.load(
                f"assets/ghosts/orange/{i+1}.png").convert_alpha()
                for i in range(8)],
            GhostColor.PINK: [pygame.image.load(
                f"assets/ghosts/pink/{i+1}.png").convert_alpha()
                for i in range(8)],
            GhostColor.SECRET: [pygame.image.load(
                f"assets/ghosts/red/{i+1}.png").convert_alpha()
                for i in range(8)],
            GhostColor.CRAZY: [
                pygame.image.load(
                    f"assets/ghosts/crazyman/{i+1}.png").convert_alpha()
                for i in range(4)]
        }

        self.alive_copy = pygame.image.load(
            "assets/icon/heart.png").convert_alpha()
        self.dead_copy = pygame.image.load(
            "assets/icon/dead_heart.png").convert_alpha()

        self.pacman_img_copy = [
            pygame.image.load(f"assets/pacman/{i}.png").convert_alpha()
            for i in range(5)
        ]

        self.fruit_copy = [
            pygame.image.load(
                f"assets/fruit/{i+1}.png"
            ).convert_alpha() for i in range(3)
        ]

        self.velocity = Parameters.PLAYER_VELOCITY
        self.movement_interval_ms: int = max(1, 1000 // self.velocity)
        self.player_move_elapsed_ms: int = 0
        self.animation_elapsed_ms: int = 0

        self.ghosts_img = self.ghosts_img_copy.copy()
        self.fruit = self.fruit_copy.copy()
        self.pacman_img: list[pygame.Surface] = self.pacman_img_copy.copy()

        PacManDrawer.update_size(self, size)

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

    def draw_maze(self):
        target_color = (150, 150, 150)
        elapsed = self.timer.crazy_mode_elapsed_time

        progress = elapsed % 1250 / 1250
        if progress > 0.5:
            progress = 1.0 - progress

        if progress:
            self.fill(tuple(int(c * progress) for c in target_color))
            bg = (255, 0, 0)
        else:
            self.fill(theme.BACKGROUND.value)
            bg = None

        for y in range(self.maze_height):
            for x in range(self.maze_width):
                self.draw_cell(
                    self.maze[y][x], (x, y), bg, None
                    if progress == 0 else progress
                )

    def draw_pacgum(self, cell: tuple[int, int], super: bool) -> None:
        x, y = cell

        px = x * self.cell_size + self.offset_x
        py = y * self.cell_size + self.offset_y

        x1, y1 = px, py
        x2, y2 = px + self.cell_size, py + self.cell_size
        if super:
            fruit_size = self.fruit[self.fruit_n].get_width()
            self.put_image(
                (x1 + fruit_size // 2, y1 + fruit_size // 2),
                self.fruit[self.fruit_n]
            )
        else:
            nc = (self.timer.elapsed_time) % 2000
            diff = 1000 - abs(1000 - nc) // 150 - 1000

            xc, yc = (x1 + x2) // 2, (y1 + y2) // 2

            self.draw_rect(
                (xc - self.cell_size // 15, yc - self.cell_size // 15 + diff),
                (xc + self.cell_size // 15, yc + self.cell_size // 15 + diff),
                theme.PACGUM.value
            )

    def draw_multiple_pacgums(
            self, cells: set[tuple[int, int]],
            super: bool = False) -> None:
        for cell in cells:
            self.draw_pacgum(cell, super=super)

    def draw_entities(self, entities: list[Entity]) -> None:
        elapsed = self.timer.elapsed_time

        for e in entities:
            e.animation_elapsed_ms = min(
                e.animation_elapsed_ms + elapsed,
                e.movement_interval_ms,
            )

            direction = e.get_direction()

            if isinstance(e, Ghost):
                if not e.is_alive:
                    continue

                color = GhostColor.CRAZY if e.crazy_mode else e.color
                params = (PacManDrawer.render_coords(elapsed, e), color)
                self.draw_ghost(*params, direction)
            else:
                self.draw_pacman(
                    PacManDrawer.render_coords(elapsed, e), direction
                )

    def update_animation(self) -> None:
        self.animation_elapsed_ms = min(
            self.animation_elapsed_ms + self.timer.elapsed_time,
            self.movement_interval_ms,
        )

    def draw_ghost(self, cell: tuple[float, float],
                   color: GhostColor, direction: Direction) -> None:
        x, y = cell

        px = int(x * self.cell_size + self.offset_x)
        py = int(y * self.cell_size + self.offset_y)

        x1, y1 = px, py
        is_jsp = self.timer.total_spend_time % 500 < 500 // 2

        if color is GhostColor.CRAZY:
            offset = 0
            if (
                self.timer.crazy_mode_elapsed_time > 3000 and
                (self.timer.crazy_mode_elapsed_time // 100) % 10 <= 5
            ):
                offset = 2

            if is_jsp:
                img = self.ghosts_img[GhostColor.CRAZY][0 + offset]
            else:
                img = self.ghosts_img[GhostColor.CRAZY][1 + offset]
        else:
            match direction:
                case Direction.SOUTH:
                    if is_jsp:
                        img = self.ghosts_img[color][0]
                    else:
                        img = self.ghosts_img[color][2]
                case Direction.NORTH:
                    if is_jsp:
                        img = self.ghosts_img[color][1]
                    else:
                        img = self.ghosts_img[color][3]
                case Direction.WEST:
                    if is_jsp:
                        img = self.ghosts_img[color][4]
                    else:
                        img = self.ghosts_img[color][6]
                case Direction.EAST:
                    if is_jsp:
                        img = self.ghosts_img[color][5]
                    else:
                        img = self.ghosts_img[color][7]
                case _:
                    img = self.ghosts_img[color][0]

        self.put_image((x1, y1), img)

    def draw_pacman(self, cell: tuple[float, float],
                    direction: Direction) -> None:
        x, y = cell

        px = int(x * self.cell_size + self.offset_x + 0.05 * self.cell_size)
        py = int(y * self.cell_size + self.offset_y + 0.05 * self.cell_size)

        x1, y1 = px, py

        n = (self.timer.total_spend_time // 70) % 8

        if n > 4:
            n = 8 - n

        if direction != self.last_pacman_direction:
            match direction:
                case Direction.NORTH:
                    self.pacman_img = self._rotate_and_scale(
                        self.pacman_img_copy, 1)
                case Direction.WEST:
                    self.pacman_img = self._rotate_and_scale(
                        self.pacman_img_copy, 2)
                case Direction.SOUTH:
                    self.pacman_img = self._rotate_and_scale(
                        self.pacman_img_copy, 3)
                case Direction.EAST:
                    self.pacman_img = self._rotate_and_scale(
                        self.pacman_img_copy, 4)

        self.put_image((x1, y1), self.pacman_img[n])

    def _rotate_and_scale(
            self, img_set: list[pygame.Surface],
            n: int) -> list[pygame.Surface]:
        return [
            pygame.transform.scale(
                rotated,
                (self.cell_size * 0.9, self.cell_size * 0.9)
            ) for rotated in (
                pygame.transform.rotate(img, 90 * n)
                for img in img_set)
        ]

    def update_size(self, new_size: tuple[int, int]) -> None:
        super().update_size(new_size)
        w, h = new_size

        for color, images in self.ghosts_img.items():
            lst = []
            for image in images:
                scaled = pygame.transform.scale(
                    image, (self.cell_size, self.cell_size)
                )
                lst.append(scaled)
            self.ghosts_img[color] = lst

        self.pacman_img = [
            pygame.transform.scale(
                img, (self.cell_size * 0.9, self.cell_size * 0.9))
            for img in self.pacman_img
        ]

        self.alive = pygame.transform.scale(
            self.alive_copy, (h // 10, h // 10)
        )

        self.dead = pygame.transform.scale(
            self.dead_copy, (h // 10, h // 10)
        )

        self.fruit = [
            pygame.transform.scale(
                fruit_img, (self.cell_size // 2, self.cell_size // 2))
            for fruit_img in self.fruit_copy
        ]
