from abc import ABC, abstractmethod
from random import choice

from ..utils import Parameters, Direction, GhostColor
from .maze import Maze


COORDINATES = tuple[int, int]


class Entity(ABC):
    default_velocity: int = Parameters.PLAYER_VELOCITY

    def __init__(
        self,
        coords: tuple[int, int],
        maze: Maze,
        velocity: int | None = None,
    ) -> None:
        self.coords: tuple[int, int] = coords
        self.maze: Maze = maze
        self.velocity: int = velocity or type(self).default_velocity
        self.player_move_elapsed_ms: int = 0
        self.movement_interval_ms: int = max(1, 1000 // self.velocity)
        self.previous_coords: tuple[int, int] = coords
        self.animation_elapsed_ms: int = 0

    @abstractmethod
    def moving(self, destination: tuple[int, int] | None) -> None:
        ...

    def can_it_move(self, elapsed_ms: int) -> bool:
        self.player_move_elapsed_ms += elapsed_ms

        if self.player_move_elapsed_ms < self.movement_interval_ms:
            return False

        self.player_move_elapsed_ms -= self.movement_interval_ms
        return True


class Player(Entity):
    direction: Direction = Direction.START
    next_direction: Direction = Direction.START

    def is_wall_here(self, direction: Direction) -> bool:
        cell = self.maze.get_cell_walls(*self.coords)
        return bool(cell & direction.value)

    def can_it_move(self, elapsed_ms: int) -> bool:
        if super().can_it_move(elapsed_ms):
            if self.next_direction is not Direction.START\
                    and not self.is_wall_here(self.next_direction):
                self.direction = self.next_direction
                self.next_direction = Direction.START
                return True
            elif not self.is_wall_here(self.direction):
                return True
        return False

    def moving(self, _: tuple[int, int] | None) -> None:
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
        self, coords: tuple[int, int], maze: Maze,
        color: GhostColor | None = None, velocity: int | None = None
    ) -> None:
        super().__init__(coords, maze, velocity)
        self.color: GhostColor = color or type(self).default_color
        self.sequence: list[tuple[int, int]] = []

    @abstractmethod
    def generate_sequence(self, destination: tuple[int, int] | None) -> None:
        ...

    def moving(self, destination: tuple[int, int] | None) -> None:
        if self.sequence == []:
            self.generate_sequence(destination)

        self.previous_coords = self.coords
        self.animation_elapsed_ms = 0

        if self.sequence != []:
            self.coords = self.sequence.pop(0)

    def pathfinding(self, end: tuple[int, int], n: int | None) -> None:
        queue: list[tuple[int, int]] = [self.coords]
        origin: dict[tuple[int, int], tuple[int, int]] = dict()
        visited: set[tuple[int, int]] = set()
        while queue:
            current = queue.pop(0)
            if current == end:
                break
            for coords in self.maze.get_available_coords(current):
                if coords in visited:
                    continue

                visited.add(coords)
                queue.append(coords)
                origin[coords] = current

        while current != self.coords:
            self.sequence.append(current)
            current = origin[current]
        self.sequence.reverse()
        if n is not None:
            self.sequence = self.sequence[:n]


class Blue(Ghost):
    default_color = GhostColor.BLUE

    def generate_sequence(self, _: tuple[int, int] | None) -> None:
        current_coords = self.coords
        last_coords: None | tuple[int, int] = None

        for i in range(30):
            available_coords = self.maze.get_available_coords(current_coords)
            if last_coords and len(available_coords) > 1:
                if last_coords in available_coords:
                    available_coords.remove(last_coords)

            last_coords = current_coords
            next_coords = choice(available_coords)

            self.sequence.append(next_coords)
            current_coords = next_coords


class Red(Ghost):
    default_color = GhostColor.RED

    def generate_sequence(self, destination: tuple[int, int] | None) -> None:
        if destination is not None:
            self.pathfinding(destination, 10)


class Green(Ghost):
    default_color = GhostColor.GREEN

    def generate_sequence(self, destination: tuple[int, int] | None) -> None:
        if destination is not None:
            self.pathfinding(destination, 2)


class Orange(Ghost):
    default_color = GhostColor.ORANGE

    def generate_sequence(self, _: tuple[int, int] | None) -> None:
        cell = choice(self.maze.get_border_cells())
        self.pathfinding(cell, None)
