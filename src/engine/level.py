
from random import shuffle, random
from typing import Callable

from .maze import Maze
from ..utils import Direction, Timer
from ..entity import Entity, Ghost, Player, Blue, Red, Pink, Orange, Secret


OPPOSITE = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST
}


class Level:
    def __init__(self, maze: Maze, t: Timer) -> None:
        self.maze: Maze = maze
        self.timer: Timer = t

        self.score: int = 0
        self.is_completed: bool = False
        self.on_crazy_mode: bool = False

        self._init_entities()
        self._init_pacgums()

    def _init_pacgums(self) -> None:
        self.pacgums: set[tuple[int, int]] = set()

        for x in range(self.maze.w):
            for y in range(self.maze.h):
                if self.maze.maze_map[y][x] == 15:
                    continue
                # self.pacgums.add((x, y))
        self.pacgums.add((2, 2))

    def _init_ghosts(self) -> None:
        ghost_classes: list[Callable] = [Blue, Red, Orange, Pink]

        shuffle(ghost_classes)

        if random() < 0.5:
            ghost_classes[0] = Secret

        for ghost_class, coords in zip(ghost_classes, self.maze.corners):
            new_ghost = ghost_class(coords, self.maze, self.timer, self.player)
            self.ghosts.append(new_ghost)
            self.entities.append(new_ghost)

    def _init_player(self) -> None:
        start_pos = ((self.maze.w // 2 - 1), (self.maze.h // 2 - 1))
        self.player = Player(start_pos, self.maze, self.timer)

        self.entities.append(self.player)

    def _init_entities(self) -> None:
        self.ghosts: list[Ghost] = []
        self.entities: list[Entity] = []

        self._init_player()
        self._init_ghosts()

    def set_crazy_mode(self, status: bool) -> None:
        self.on_crazy_mode = status

        for e in self.entities:
            e.crazy_mode = status

    def change_direction(self, new_direction: Direction) -> None:
        if self.player.direction != Direction.START\
                and OPPOSITE.get(self.player.direction) == new_direction:
            self.player.reverse(new_direction)
        else:
            self.player.next_direction = new_direction

    def check_crazy_mode(self) -> None:
        if self.on_crazy_mode is True:
            self.timer.crazy_mode_elapsed_time += self.timer.elapsed_time
            if self.timer.crazy_mode_elapsed_time >= 5000:
                self.timer.crazy_mode_elapsed_time = 0
                self.set_crazy_mode(False)

    def check_collision(self) -> None:
        for g in self.ghosts:
            if not g.is_alive:
                continue
            if g.coords == self.player.coords:
                if self.on_crazy_mode:
                    self.score += 200
                    g.respawn()
                else:
                    self.player.is_alive = False

    def is_pacgum_here(self) -> None:
        if self.player.coords in self.pacgums:
            if self.player.coords in self.maze.corners:
                self.set_crazy_mode(True)
                self.timer.crazy_mode_elapsed_time = 0
                self.score += 200
            else:
                self.score += 20

            self.pacgums.remove(self.player.coords)

        if not self.pacgums:
            self.is_completed = True

    def update(self) -> None:
        self.check_crazy_mode()

        self.player.moving()

        self.check_collision()

        for g in self.ghosts:
            g.moving()

        self.is_pacgum_here()
