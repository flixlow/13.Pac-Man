
from random import shuffle
from typing import Callable

from .maze import MazeLevel
from .utils import Direction, State
from .parsing import Config
from .entity import Entity, Ghost, Player, Blue, Red, Green, Orange


class Game:
    def __init__(self, config: Config, level: MazeLevel) -> None:
        self.config: Config = config
        self.level: MazeLevel = level
        self._init_entities()

    def _init_ghosts(self) -> None:
        ghost_classes: list[Callable] = [Blue, Red, Orange, Green]

        shuffle(ghost_classes)
        for ghost_class, c in zip(ghost_classes, self.level.corners):
            self.entities.append(ghost_class(c, self.level))

    def _init_player(self) -> None:
        start_pos = ((self.level.w // 2 - 1), (self.level.h // 2 - 1))
        self.player = Player(start_pos, self.level)

        self.entities.append(self.player)

    def _init_pacgums(self) -> None:
        self.pacgums: set[tuple[int, int]] = set()

        for x in range(self.level.w):
            for y in range(self.level.h):
                if self.level.maze[y][x] == 15:
                    continue
                self.pacgums.add((x, y))

    def _init_entities(self) -> None:
        self.entities: list[Entity] = []

        self._init_ghosts()
        self._init_player()
        self._init_pacgums()

    def change_direction(self, direction: Direction) -> None:
        if not self.player.is_wall_here(direction):
            self.player.direction = direction
        else:
            self.player.next_direction = direction

    def moving_entities(self, elapsed_time: int) -> None:
        for entity in self.entities:
            if entity.can_it_move(elapsed_time):
                entity.moving()
            if isinstance(entity, Player):
                self.pacgums.discard(entity.coords)

    def check_hitbox(self) -> None:
        for entity in self.entities:
            if isinstance(entity, Ghost):
                if entity.coords == self.player.coords:
                    self.player_state.lives -= 1
                    self.state = State.PAUSE
                elif self.player_state.lives <= 0:
                    self.enter_your_name()
                    self.state = State.PAUSE
