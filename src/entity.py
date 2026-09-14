from abc import ABC, abstractmethod
from random import choice

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
        self.previous_coords: tuple[int, int] = coords
        self.animation_elapsed_ms: int = self.movement_interval_ms

    @abstractmethod
    def moving(self) -> None:
        ...

    def get_cell_walls(self, coords: tuple[int, int]) -> int:
        x, y = coords
        return self.maze[y][x]

    def can_it_move(self, elapsed_ms: int) -> bool:
        self.player_move_elapsed_ms += elapsed_ms

        if self.player_move_elapsed_ms < self.movement_interval_ms:
            return False

        self.player_move_elapsed_ms -= self.movement_interval_ms
        return True

    def update_animation(self, elapsed_ms: int) -> None:
        self.animation_elapsed_ms = min(
            self.animation_elapsed_ms + elapsed_ms,
            self.movement_interval_ms,
        )

    def render_coords(self) -> tuple[float, float]:
        progress = self.animation_elapsed_ms / self.movement_interval_ms
        start_x, start_y = self.previous_coords
        end_x, end_y = self.coords
        return (
            start_x + (end_x - start_x) * progress,
            start_y + (end_y - start_y) * progress,
        )


class Player(Entity):
    default_velocity: int = Parameters.PLAYER_VELOCITY
    direction: Direction = Direction.START

    def is_wall_here(self, coords: tuple[int, int]) -> bool:
        cell = self.get_cell_walls(coords)
        return bool(cell & self.direction.value)

    def can_it_move(self, elapsed_ms: int) -> bool:
        return super().can_it_move(elapsed_ms) and not self.is_wall_here(self.coords)

    def moving(self) -> None:
        x, y = self.coords
        self.previous_coords = self.coords
        self.animation_elapsed_ms = 0
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
    def generate_sequence(self) -> None:
        ...

    def moving(self) -> None:
        if self.sequence == []:
            self.generate_sequence()
        if self.sequence != []:
            self.coords = self.sequence.pop(0)


class Blue(Ghost):
    default_color = GhostColor.BLUE

    def get_available_coords(self, last_coords: tuple[int, int]) -> list[tuple[int, int]]:
        coords: list[tuple[int, int]] = []
        x, y = last_coords

        cell = self.get_cell_walls(last_coords)
        if not cell & Direction.NORTH.value:
            coords.append((x, y - 1))
        if not cell & Direction.EAST.value:
            coords.append((x + 1, y))
        if not cell & Direction.SOUTH.value:
            coords.append((x, y + 1))
        if not cell & Direction.WEST.value:
            coords.append((x - 1, y))

        return coords

    def generate_sequence(self) -> None:
        current_coords = self.coords
        last_coords: None | tuple[int, int] = None

        for _ in range(30):
            available_coords = self.get_available_coords(current_coords)
            if last_coords and len(available_coords) > 1:
                if last_coords in available_coords:
                    available_coords.remove(last_coords)

            last_coords = current_coords
            next_coords = choice(available_coords)

            self.sequence.append(next_coords)
            current_coords = next_coords


class Red(Ghost):
    default_color = GhostColor.RED

    def generate_sequence(self) -> None:
        pass


class Green(Ghost):
    default_color = GhostColor.GREEN

    def generate_sequence(self) -> None:
        pass


class Orange(Ghost):
    default_color = GhostColor.ORANGE

    def generate_sequence(self) -> None:
        pass
