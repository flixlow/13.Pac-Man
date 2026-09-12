from abc import ABC, abstractmethod

from .utils import Parameters, Direction, GhostColor


class Entity(ABC):
    default_velocity: int = Parameters.PLAYER_VELOCITY

    def __init__(
        self,
        coords: tuple[int, int],
        maze: list[list[int]],
        velocity: int | None = None,
    ) -> None:
        self.coords: tuple[int, int] = coords
        self.maze: list[list[int]] = maze
        self.velocity: int = velocity or type(self).default_velocity
        self.movement_interval_ms: int = 1000 // self.velocity
        self.player_move_elapsed_ms: int = 0

    @abstractmethod
    def moving(self) -> None:
        ...

    def can_it_move(self, elapsed_ms: int) -> bool:
        self.player_move_elapsed_ms += elapsed_ms

        if self.player_move_elapsed_ms < self.movement_interval_ms:
            return False

        self.player_move_elapsed_ms -= self.movement_interval_ms
        return True


class Player(Entity):
    default_velocity: int = Parameters.PLAYER_VELOCITY
    direction: Direction = Direction.START

    def get_cell_walls(self, coords: tuple[int, int]) -> int:
        x, y = coords
        return self.maze[y][x]

    def is_wall_here(self) -> bool:
        cell = self.get_cell_walls(self.coords)
        return bool(cell & self.direction.value)

    def can_it_move(self, elapsed_ms: int) -> bool:
        return super().can_it_move(elapsed_ms) and not self.is_wall_here()

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
    default_velocity: int = Parameters.GHOST_VELOCITY
    default_color: GhostColor = GhostColor.SECRET

    def __init__(
        self, coords: tuple[int, int], maze: list[list[int]],
        color: GhostColor | None = None, velocity: int | None = None
    ) -> None:
        super().__init__(coords, maze, velocity)
        self.color: GhostColor = color or type(self).default_color
        self.sequence: list[tuple[int, int]] = []

    @abstractmethod
    def generate_sequence(
            self, maze: list[list[int]]) -> list[tuple[int, int]]:
        ...

    def moving(self) -> None:
        self.coords


class Blue(Ghost):
    default_color = GhostColor.BLUE

    def generate_sequence(
            self, maze: list[list[int]]) -> list[tuple[int, int]]:
        return []


class Red(Ghost):
    default_color = GhostColor.RED

    def generate_sequence(
            self, maze: list[list[int]]) -> list[tuple[int, int]]:
        return []


class Green(Ghost):
    default_color = GhostColor.GREEN

    def generate_sequence(
            self, maze: list[list[int]]) -> list[tuple[int, int]]:
        return []


class Orange(Ghost):
    default_color = GhostColor.ORANGE

    def generate_sequence(
            self, maze: list[list[int]]) -> list[tuple[int, int]]:
        return []
