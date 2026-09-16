
from random import shuffle
from typing import Callable

from .maze import Maze
from .utils import Direction
from .parsing import Config
from .entity import Entity, Ghost, Player, Blue, Red, Green, Orange


class Level:
    def __init__(self, config: Config, level: Maze) -> None:
        self.config: Config = config
        self.level: Maze = level

        self.crazy_mode: bool = False
        self.score: int = 0
        self.alive: bool = True
        self.game_end: bool = False

        self._init_entities()
        self._init_pacgums()

    def _init_ghosts(self) -> None:
        ghost_classes: list[Callable] = [Blue]  #, Red, Orange, Green]

        shuffle(ghost_classes)
        for ghost_class, coords in zip(ghost_classes, self.level.corners):
            new_ghost = ghost_class(coords, self.level)
            self.ghosts.append(new_ghost)
            self.entities.append(new_ghost)

    def _init_player(self) -> None:
        start_pos = ((self.level.w // 2 - 1), (self.level.h // 2 - 1))
        self.player = Player(start_pos, self.level)

        self.entities.append(self.player)

    def _init_entities(self) -> None:
        self.ghosts: list[Ghost] = []
        self.entities: list[Entity] = []

        self._init_ghosts()
        self._init_player()

    def _init_pacgums(self) -> None:
        self.pacgums: set[tuple[int, int]] = set()

        for x in range(self.level.w):
            for y in range(self.level.h):
                if self.level.maze[y][x] == 15:
                    continue
                self.pacgums.add((x, y))

    def get_ghosts_coords(self) -> set[tuple[int, int]]:
        return {ghost.coords for ghost in self.ghosts}

    def change_direction(self, direction: Direction) -> None:
        if not self.player.is_wall_here(direction):
            self.player.direction = direction
        else:
            self.player.next_direction = direction

    def is_pacgum_here(self) -> None:
        if self.player.coords in self.pacgums:
            if self.player.coords in self.level.corners:
                self.crazy_mode = True
                self.score += 200
            else:
                self.score += 20
            self.pacgums.remove(self.player.coords)
        if not self.pacgums:
            self.game_end = True

    def moving_entities(self, elapsed_time: int) -> None:
        for entity in self.entities:
            if entity.can_it_move(elapsed_time):
                entity.moving()

        if self.player.coords in self.get_ghosts_coords():
            self.alive = False

        self.is_pacgum_here()

    def check_hitbox(self) -> None:
        for entity in self.entities:
            if isinstance(entity, Ghost):
                pass
