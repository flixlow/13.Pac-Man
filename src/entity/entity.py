"""Base class for every moving entity in the maze."""

from abc import ABC, abstractmethod

from ..engine.maze import Maze
from ..utils import Direction, Timer


class Entity(ABC):
    """Abstract base class for game entities such as Pac-Man and ghosts.

    Args:
        coords: Starting coordinates inside the maze.
        maze: Maze instance used for collision checks.
        t: Shared timer.
    """

    is_alive: bool = True
    default_velocity: int = 3

    def __init__(self, coords: tuple[int, int], maze: Maze, t: Timer) -> None:
        """Initialize the entity state.

        Args:
            coords: Initial position on the grid.
            maze: Maze containing the entity.
            t: Timer used by the entity.
        """
        self.timer: Timer = t
        self.maze: Maze = maze
        self.crazy_mode: bool = False
        self.animation_elapsed_ms: int = 0
        self.coords: tuple[int, int] = coords
        self.previous_coords: tuple[int, int] = coords
        self.starting_coords: tuple[int, int] = coords
        self.velocity: int = type(self).default_velocity
        self.movement_interval_ms: int = max(1, 1000 // self.velocity)

    @abstractmethod
    def move(self) -> None:
        """Advance the entity by one simulation step."""

    @property
    def progress(self) -> float:
        """Return the interpolation progress of the current movement step."""
        return min(
            self.animation_elapsed_ms / max(1, self.movement_interval_ms), 1.0
        )

    def get_direction(self) -> Direction:
        """Infer the direction from the delta between previous and current pos.

        Returns:
            Direction corresponding to the displacement.
        """
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
        """Check whether the entity can perform a movement step.

        Returns:
            True if movement progress is complete.
        """
        return self.progress == 1
