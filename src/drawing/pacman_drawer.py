
import pygame
from random import randint

from ..engine.maze import Maze
from ..entity import Ghost, Entity
from .maze_drawer import MazeDrawer
from ..color_utils import ThemeSelection
from ..utils import GhostColor, Parameters, Direction, Timer
from ..assetloader import AssetLoader

Pos = tuple[int, int]
Color = tuple[int, int, int]


class PacManDrawer(MazeDrawer):
    def __init__(self, size: tuple[int, int], maze: Maze,
                 t: Timer, theme_selection: ThemeSelection) -> None:
        super().__init__(size, maze, theme_selection)

        self.timer = t
        self.last_pacman_direction: Direction = Direction.START

        # Assets
        self.ghosts_img_copy = AssetLoader.load_ghosts()
        self.pacman_img_copy: list[pygame.Surface] = AssetLoader.load_pacman()
        self.dead_copy, self.alive_copy = AssetLoader.load_life()
        self.fruit_copy = AssetLoader.load_fruit()
        self.bg_msg_copy: pygame.Surface = AssetLoader.load_buttons()[0]

        self.chosen_fruit = randint(0, len(self.fruit_copy) - 1)

        # Time
        self.velocity = Parameters.PLAYER_VELOCITY
        self.movement_interval_ms: int = max(1, 1000 // self.velocity)
        self.player_move_elapsed_ms: int = 0
        self.animation_elapsed_ms: int = 0

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
            self.fill(self.theme.background)
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
            fruit_size = self.fruit[self.chosen_fruit].get_width()
            self.put_image(
                (x1 + fruit_size // 2, y1 + fruit_size // 2),
                self.fruit[self.chosen_fruit]
            )
        else:
            nc = (self.timer.total_spend_time) % 2000
            diff = (1000 - abs(1000 - nc) // 100 - 1000) * 20

            xc, yc = (x1 + x2) // 2, (y1 + y2) // 2

            color = tuple(
                min(255, max(c + diff, 0)) for c in self.theme.theme.pacgum)

            self.draw_rect(
                (xc - self.cell_size // 15, yc - self.cell_size // 15),
                (xc + self.cell_size // 15, yc + self.cell_size // 15),
                color
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

        self.ghosts_img: dict[GhostColor, pygame.Surface] = {}

        for color, images in self.ghosts_img_copy.items():
            lst = []
            for i, image in enumerate(images):
                scaled = pygame.transform.scale(
                    image, (self.cell_size, self.cell_size)
                )
                lst.append(scaled)
            self.ghosts_img[color] = lst

        self.pacman_img = [
            pygame.transform.scale(
                img, (self.cell_size * 0.9, self.cell_size * 0.9))
            for img in self.pacman_img_copy
        ]

        self.alive = pygame.transform.scale(
            self.alive_copy, (w // 20, w // 20)
        )

        self.dead = pygame.transform.scale(
            self.dead_copy, (w // 20, w // 20)
        )

        self.fruit = [
            pygame.transform.scale(
                fruit_img, (self.cell_size // 2, self.cell_size // 2))
            for fruit_img in self.fruit_copy
        ]

    def press_space_to_restart(self, msg: str) -> None:
        w, h = self.size

        self.font_press = pygame.font.Font("assets/font/title.otf", w // 25)
        w_text, h_text = self.font_press.size(msg)
        self.padding_x, self.padding_y = w // 15, h // 15
        self.bg_msg = pygame.transform.scale(
            self.bg_msg_copy,
            (w_text + self.padding_x, h_text + self.padding_y)
        )

        rendered = self.font_press.render(msg, True, (255, 255, 255))
        w_text, h_text = rendered.get_size()
        self.put_image(
            (
                w // 2 - w_text // 2 - self.padding_x // 2,
                h // 2 - h_text // 2 - self.padding_y // 2
            ), self.bg_msg)

        self.surface.blit(
            rendered, (w // 2 - w_text // 2, h // 2 - h_text // 2)
        )

    def draw_ghost_path(self, color: GhostColor, path: list[Pos]) -> None:
        color_match: dict[GhostColor, Color] = {
            GhostColor.BLUE: (0, 0, 255),
            GhostColor.ORANGE: (255, 127, 0),
            GhostColor.RED: (255, 0, 0),
            GhostColor.PINK: (255, 127, 127),
            GhostColor.SECRET: (0, 0, 0)
        }

        for i, (x, y) in enumerate(path):
            progress = i / len(path)
            selected = list(color_match[color])
            for i in range(len(selected)):
                selected[i] = min(255, max(0, progress * selected[i]))
            self.draw_cell(self.maze[y][x], (x, y), bg=selected)
