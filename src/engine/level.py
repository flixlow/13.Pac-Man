
from random import shuffle
from typing import Callable

from .maze import Maze
from ..utils import Direction
from ..entity import Entity, Ghost, Player, Blue, Red, Green, Orange


class Level:
    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze

        self.score: int = 0
        self.on_crazy_mode: bool = False
        self.is_completed: bool = False
        self.is_dead: bool = False

        self._init_entities()
        self._init_pacgums()

    def _init_ghosts(self) -> None:
        ghost_classes: list[Callable] = [Blue, Green, Red, Orange]

        shuffle(ghost_classes)
        for ghost_class, coords in zip(ghost_classes, self.maze.corners):
            new_ghost = ghost_class(coords, self.maze)
            self.ghosts.append(new_ghost)
            self.entities.append(new_ghost)

    def _init_player(self) -> None:
        start_pos = ((self.maze.w // 2 - 1), (self.maze.h // 2 - 1))
        self.player = Player(start_pos, self.maze)

        self.entities.append(self.player)

    def _init_entities(self) -> None:
        self.ghosts: list[Ghost] = []
        self.entities: list[Entity] = []

        self._init_ghosts()
        self._init_player()

    def _init_pacgums(self) -> None:
        self.pacgums: set[tuple[int, int]] = set()

        for x in range(self.maze.w):
            for y in range(self.maze.h):
                if self.maze.maze[y][x] == 15:
                    continue
                self.pacgums.add((x, y))

    def get_ghosts_coords(self) -> set[tuple[int, int]]:
        return {ghost.coords for ghost in self.ghosts}

    def change_direction(self, direction: Direction) -> None:
        self.player.next_direction = direction

    def is_pacgum_here(self) -> None:
        if self.player.coords in self.pacgums:
            if self.player.coords in self.maze.corners:
                self.crazy_mode = True
                self.score += 200
            else:
                self.score += 20
            self.pacgums.remove(self.player.coords)
        if not self.pacgums:
            self.is_completed = True

    def moving_entities(self, elapsed_time: int) -> None:
        for entity in self.entities:
            if entity.can_it_move(elapsed_time):
                entity.moving()

        if self.player.coords in self.get_ghosts_coords():
            self.is_dead = True

        self.is_pacgum_here()
