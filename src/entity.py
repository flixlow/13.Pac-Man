from abc import ABC, abstractmethod
from pathlib import Path

from .utils import Paths, Parameters


class Entity(ABC):
    def __init__(
            self, asset_file: str, coords: tuple[int, int], velocity: int
            ) -> None:
        self.asset_file: Path = Path(asset_file)
        self.coords: tuple[int, int] = coords
        self.velocity: int = velocity


class Ghost(Entity):
    def __init__(
            self, asset_file: str, coords: tuple[int, int], velocity: int
            ) -> None:
        super().__init__(asset_file, coords, velocity)

    @abstractmethod
    def moving(self) -> list[tuple[int]]:
        ...


class Blue(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        asset_file: str = Paths.BLUE,
        velocity: int = Parameters.GHOST_VELOCITY
    ) -> None:
        super().__init__(asset_file, coords, velocity)

    def moving(self) -> list[tuple[int]]:
        return []


class Red(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        asset_file: str = Paths.RED,
        velocity: int = Parameters.GHOST_VELOCITY
    ) -> None:
        super().__init__(asset_file, coords, velocity)

    def moving(self) -> list[tuple[int]]:
        return []


class Green(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        asset_file: str = Paths.GREEN,
        velocity: int = Parameters.GHOST_VELOCITY
    ) -> None:
        super().__init__(asset_file, coords, velocity)

    def moving(self) -> list[tuple[int]]:
        return []


class Orange(Ghost):
    def __init__(
        self,
        coords: tuple[int, int],
        asset_file: str = Paths.ORANGE,
        velocity: int = Parameters.GHOST_VELOCITY
    ) -> None:
        super().__init__(asset_file, coords, velocity)

    def moving(self) -> list[tuple[int]]:
        return []


class Player(Entity):
    def __init__(
        self,
        coords: tuple[int, int],
        asset_file: str = Paths.PACMAN,
        velocity: int = Parameters.PLAYER_VELOCITY
    ) -> None:
        super().__init__(asset_file, coords, velocity)
