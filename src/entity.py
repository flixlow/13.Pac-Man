from abc import ABC, abstractmethod
from pathlib import Path


class Entity(ABC):
    def __init__(
            self, asset_file: str, velocity: int, coords: tuple[int, int]
            ) -> None:
        self.asset_file: Path = Path(asset_file)
        self.velocity: int = velocity
        self.coords: tuple[int, int] = coords


class Ghost(Entity):
    def __init__(
            self, asset_file: str, velocity: int, coords: tuple[int, int]
            ) -> None:
        super().__init__(asset_file, velocity, coords)

    @abstractmethod
    def moving(self) -> list[tuple[int]]:
        ...


class Player(Entity):
    def __init__(
            self, asset_file: str, velocity: int, coords: tuple[int, int]
            ) -> None:
        super().__init__(asset_file, velocity, coords)
