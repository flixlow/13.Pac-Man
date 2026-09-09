import pygame
from random import shuffle
from typing import Callable
from enum import Enum, auto

from .scorer import Scorer
from .parsing import Parser, Config
from .pacman_drawer import PacManDrawer, Ghost
from .entity import Entity, Player, Blue, Red, Green, Orange


class Direction(Enum):
    START = auto()
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.maze_index: int = 0
        self.config_file = config_file
        self.config: Config = Parser(self.config_file).open()
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.entities: list[Entity] = self._init_entities()

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

    def _init_entities(self) -> list[Entity]:
        entities: list[Entity] = []
        w = self.config.levels[self.maze_index].width
        h = self.config.levels[self.maze_index].height
        ghosts: list[Callable] = [Blue, Red, Orange, Green]
        coords: set[tuple[int, int]] = {(0, 0), (0, h), (w, 0), (w, h)}

        shuffle(ghosts)
        for ghost_class, c in zip(ghosts, coords):
            entities.append(ghost_class(c))

        self.player: Player = Player(((w // 2 - 1), (h // 2 - 1)))
        entities.append(self.player)

        return entities

    def check_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player_movement(Direction.NORTH)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player_movement(Direction.SOUTH)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player_movement(Direction.WEST)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player_movement(Direction.EAST)

            if event.type == pygame.VIDEORESIZE:
                w, h = event.size
                self.pacman_frame.update_size((w, h - h // 10))
                self.pacman_frame.draw_maze()

        return True

    def player_movement(self, direction: Direction) -> None:
        x = self.player.coords[0]
        y = self.player.coords[1]
        cell: int = self.config.mazes[self.maze_index][y][x]
        self.pacman_frame.draw_cell(cell, self.player.coords, bg=True)

        match direction:
            case Direction.NORTH:
                if not cell & 1:
                    self.pacman_frame
                    self.player.coords = (x, y - 1)
            case Direction.EAST:
                if not cell & 2:
                    self.player.coords = (x + 1, y)
            case Direction.SOUTH:
                if not cell & 4:
                    self.player.coords = (x, y + 1)
            case Direction.WEST:
                if not cell & 8:
                    self.player.coords = (x - 1, y)

    def main_loop(self) -> None:
        while self.running:
            self.running = self.check_events()

            self.pacman_frame.draw_ghost((2, 2), Ghost.SECRET)
            self.pacman_frame.draw_pacman(self.player.coords)
            self.screen.blit(self.pacman_frame.surface, (0, 0))
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
