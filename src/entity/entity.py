
from abc import ABC, abstractmethod

from ..engine.maze import Maze
from ..utils import Direction, Timer


class Entity(ABC):
    is_alive: bool = True
    default_velocity: int = 3

    def __init__(self, coords: tuple[int, int], maze: Maze, t: Timer) -> None:
        self.timer: Timer = t
        self.maze: Maze = maze
        self.crazy_mode: bool = False
        self.animation_elapsed_ms: int = 0
        self.player_move_elapsed_ms: int = 0
        self.coords: tuple[int, int] = coords
        self.previous_coords: tuple[int, int] = coords
        self.starting_coords: tuple[int, int] = coords
        self.velocity: int = type(self).default_velocity
        self.movement_interval_ms: int = max(1, 1000 // self.velocity)

    @abstractmethod
    def moving(self) -> None:
        ...

    def get_direction(self) -> Direction:
        diff = (
            self.coords[0] - self.previous_coords[0],
            self.coords[1] - self.previous_coords[1]
        )
        match diff:
            case (-1, 0):
                return Direction.WEST
            case (1, 0):
                return Direction.EAST
            case (0, -1):
                return Direction.NORTH
            case (0, 1):
                return Direction.SOUTH
            case _:
                return Direction.START

    def can_it_move(self) -> bool:
        self.player_move_elapsed_ms += self.timer.elapsed_time

        if self.player_move_elapsed_ms < self.movement_interval_ms:
            return False

        self.player_move_elapsed_ms -= self.movement_interval_ms
        return True
