from abc import ABC, abstractmethod

from .drawing.pacman_drawer import GhostColor
from .utils import Parameters, Direction


class Entity(ABC):
    def __init__(self, coords: tuple[int, int], velocity: int) -> None:
        self.coords: tuple[int, int] = coords
        self.velocity: int = velocity


class Player(Entity):
    def __init__(
        self,
        coords: tuple[int, int],
        velocity: int = Parameters.PLAYER_VELOCITY
    ) -> None:
        super().__init__(coords, velocity)
        self.direction: Direction = Direction.START
        self.movement_interval_ms: int = 1000 // self.velocity
        self.player_move_elapsed_ms: int = 0

    def can_it_move(self, elapsed_ms: int) -> bool:
        self.player_move_elapsed_ms += elapsed_ms

        if self.player_move_elapsed_ms < self.movement_interval_ms:
            return False

        self.player_move_elapsed_ms -= self.movement_interval_ms
        return True


    def moving(self) -> None:
        x, y = self.coords
        match self.direction:
            case Direction.NORTH:
                self.coords = (x, y - 1)
            case Direction.WEST:
                self.coords = (x - 1, y)
            case Direction.SOUTH:
                self.coords = (x, y + 1)
            case Direction.EAST:
                self.coords = (x + 1, y)


class Ghost(Entity):
    def __init__(
        self,
        coords: tuple[int, int],
        color: GhostColor,
        velocity: int = Parameters.GHOST_VELOCITY
    ) -> None:
        super().__init__(coords, velocity)
        self.color: GhostColor = color
        self.sequence: list[tuple[int, int]] = []

    @abstractmethod
    def generate_sequence(
            self, maze: list[list[int]]) -> list[tuple[int, int]]:
        ...

    def moving(self) -> None:
        self.coords


class Blue(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        color: GhostColor = GhostColor.BLUE,
    ) -> None:
        super().__init__(coords, color)

    def generate_sequence(
            self, maze: list[list[int]]) -> list[tuple[int, int]]:
        return []


class Red(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        color: GhostColor = GhostColor.RED,
    ) -> None:
        super().__init__(coords, color)

    def generate_sequence(
            self, maze: list[list[int]]) -> list[tuple[int, int]]:
        return []


class Green(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        color: GhostColor = GhostColor.GREEN,
    ) -> None:
        super().__init__(coords, color)

    def generate_sequence(
            self, maze: list[list[int]]) -> list[tuple[int, int]]:
        return []


class Orange(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        color: GhostColor = GhostColor.ORANGE,
    ) -> None:
        super().__init__(coords, color)

    def generate_sequence(
            self, maze: list[list[int]]) -> list[tuple[int, int]]:
        return []
