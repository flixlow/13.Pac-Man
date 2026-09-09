from abc import ABC, abstractmethod

from .pacman_drawer import GhostColor
from .utils import Parameters


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


class Ghost(Entity):
    def __init__(
        self,
        coords: tuple[int, int],
        color: GhostColor,
        velocity: int = Parameters.GHOST_VELOCITY
    ) -> None:
        super().__init__(coords, velocity)
        self.color: GhostColor = color

    @abstractmethod
    def moving(self) -> list[tuple[int]]:
        ...


class Blue(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        color: GhostColor = GhostColor.BLUE,
    ) -> None:
        super().__init__(coords, color)

    def moving(self) -> list[tuple[int]]:
        return []


class Red(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        color: GhostColor = GhostColor.RED,
    ) -> None:
        super().__init__(coords, color)

    def moving(self) -> list[tuple[int]]:
        return []


class Green(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        color: GhostColor = GhostColor.GREEN,
    ) -> None:
        super().__init__(coords, color)

    def moving(self) -> list[tuple[int]]:
        return []


class Orange(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        color: GhostColor = GhostColor.ORANGE,
    ) -> None:
        super().__init__(coords, color)

    def moving(self) -> list[tuple[int]]:
        return []
