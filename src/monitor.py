import pygame
from random import shuffle
from typing import Callable

from .scorer import Scorer
from .utils import Direction
from .parsing import parsing, Config
from .drawing.pacman_drawer import PacManDrawer
from .entity import Ghost, Player, Blue, Red, Green, Orange


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.maze_index: int = 0
        self.config_file = config_file
        self.config: Config = parsing(self.config_file)
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.ghosts: list[Ghost] = self._init_entities()

        pygame.init()
        self.pygame_info = pygame.display.Info()
        self.screen_size = (
            self.pygame_info.current_w // 2,
            self.pygame_info.current_h // 2
        )
        self.header = self.screen_size[1]//5

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.RESIZABLE
        )

        self.running = True

        h, w = self.screen_size
        self.pacman_frame = PacManDrawer((h, w - self.header), self.config)
        self.pacman_frame.draw_maze()
        self.key_directions: dict[int, Direction] = {
            pygame.K_UP: Direction.NORTH,
            pygame.K_w: Direction.NORTH,
            pygame.K_RIGHT: Direction.EAST,
            pygame.K_d: Direction.EAST,
            pygame.K_DOWN: Direction.SOUTH,
            pygame.K_s: Direction.SOUTH,
            pygame.K_LEFT: Direction.WEST,
            pygame.K_a: Direction.WEST,
        }

    def _init_entities(self) -> list[Ghost]:
        ghosts: list[Ghost] = []
        w = self.config.levels[self.maze_index].width
        h = self.config.levels[self.maze_index].height
        ghost_classes: list[Callable] = [Blue, Red, Orange, Green]
        coords = {(0, 0), (0, (h - 1)), ((w - 1), 0), ((w - 1), (h - 1))}

        shuffle(ghost_classes)
        for ghost_class, c in zip(ghost_classes, coords):
            ghosts.append(ghost_class(c))

        self.player: Player = Player(((w // 2 - 1), (h // 2 - 1)))

        return ghosts

    def check_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key in self.key_directions:
                    new_direction = self.key_directions[event.key]
                    if not self.is_there_a_wall_here(new_direction):
                        self.player.direction = new_direction

            if event.type == pygame.VIDEORESIZE:
                w, h = event.size
                self.pacman_frame.update_size((w, h - h // 10))
                self.pacman_frame.draw_maze()

        return True

    def get_cell_walls(self, coords: tuple[int, int]) -> int:
        x, y = coords
        return self.config.mazes[self.maze_index][y][x]

    def is_there_a_wall_here(self, direction: Direction) -> bool:
        cell = self.get_cell_walls(self.player.coords)
        return bool(cell & direction.value)

    def display_entities(self) -> None:
        for ghost in self.ghosts:
            self.pacman_frame.draw_ghost(ghost.coords, ghost.color)

        if not self.is_there_a_wall_here(self.player.direction):
            cell = self.get_cell_walls(self.player.coords)

            self.pacman_frame.draw_cell(cell, self.player.coords, bg=True)

            self.player.moving()

            self.pacman_frame.draw_pacman(self.player.coords)

    def main_loop(self) -> None:
        while self.running:

            self.running = self.check_events()

            self.display_entities()

            self.screen.blit(self.pacman_frame.surface, (0, 0))

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
