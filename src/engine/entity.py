from abc import ABC, abstractmethod
from random import choice

from ..utils import Parameters, Direction, GhostColor
from .maze import Maze


class Entity(ABC):
    default_velocity: int = 3

    def __init__(self, coords: tuple[int, int], maze: Maze) -> None:
        self.maze: Maze = maze
        self.crazy_mode: bool = False
        self.animation_elapsed_ms: int = 0
        self.player_move_elapsed_ms: int = 0
        self.coords: tuple[int, int] = coords
        self.previous_coords: tuple[int, int] = coords
        self.velocity: int = type(self).default_velocity
        self.movement_interval_ms: int = max(1, 1000 // self.velocity)

    @abstractmethod
    def moving(self, elapsed_time: int) -> None:
        ...

    def can_it_move(self, elapsed_ms: int) -> bool:
        self.player_move_elapsed_ms += elapsed_ms

        if self.player_move_elapsed_ms < self.movement_interval_ms:
            return False

        self.player_move_elapsed_ms -= self.movement_interval_ms
        return True

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


class Player(Entity):
    direction: Direction = Direction.START
    next_direction: Direction = Direction.START
    default_velocity: int = Parameters.PLAYER_VELOCITY

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

    def moving(self, elapsed_time: int) -> None:
        if not self.can_it_move(elapsed_time):
            return
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
            self, coords: tuple[int, int], maze: Maze, player: Player) -> None:
        super().__init__(coords, maze)
        self.player: Player = player
        self.color: GhostColor = type(self).default_color
        self.sequence: list[tuple[int, int]] = []

    @abstractmethod
    def generate_sequence(self) -> None:
        ...

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

    def get_direction_away_from(self) -> None:
        x, y = self.player.coords

        availables = self.maze.get_available_coords(self.coords)

        cell = max(availables, key=lambda c: (abs(c[0] - x) + (abs(c[1] - y))))

        self.sequence = [cell]

    def moving(self, elapsed_time: int) -> None:
        if not self.can_it_move(elapsed_time):
            return

        if self.crazy_mode:
            self.get_direction_away_from()
        elif self.sequence == []:
            self.generate_sequence()

        self.animation_elapsed_ms = 0
        self.previous_coords = self.coords
        if self.sequence:
            self.coords = self.sequence.pop(0)


class Secret(Ghost):
    default_color = GhostColor.SECRET

    def teleportate(self, pos: tuple[int, int]) -> None:
        neightbour_cells = self.maze.get_neighbour_cells(pos, 2)

        self.sequence = [choice(list(neightbour_cells))]

    def generate_sequence(self) -> None:
        self.pathfinding(self.player.coords, None)

        if len(self.sequence) >= 15:
            self.teleportate(self.player.coords)


class Blue(Ghost):
    default_color = GhostColor.BLUE

    def generate_sequence(self) -> None:
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
    default_color = GhostColor.SECRET

    def generate_sequence(self) -> None:
        self.pathfinding(self.player.coords, 15)


class Pink(Ghost):
    default_color = GhostColor.PINK

    def generate_sequence(self) -> None:
        self.pathfinding(self.player.coords, 5)


class Orange(Ghost):
    default_color = GhostColor.ORANGE

    def generate_sequence(self) -> None:
        cell = choice(self.maze.get_border_cells())
        self.pathfinding(cell, None)
