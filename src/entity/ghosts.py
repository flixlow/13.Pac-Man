
from random import choice
from abc import abstractmethod

from .entity import Entity
from .player import Player
from ..engine.maze import Maze
from ..utils import GhostColor, Parameters


class Ghost(Entity):
    default_velocity: int = Parameters.GHOST_VELOCITY
    default_color: GhostColor = GhostColor.SECRET

    def __init__(
            self, coords: tuple[int, int], maze: Maze, player: Player) -> None:
        super().__init__(coords, maze)
        self.color: GhostColor = type(self).default_color
        self.sequence: list[tuple[int, int]] = []
        self.player: Player = player
        self.respawn_timer: int = 0

    @abstractmethod
    def generate_sequence(self) -> None:
        ...

    def respawn(self) -> None:
        self.is_alive = False
        self.respawn_timer = 0
        self.crazy_mode = False
        self.coords = self.starting_coords
        self.previous_coords = self.starting_coords

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

        if not self.is_alive:
            self.respawn_timer += elapsed_time
            if self.respawn_timer >= 200:
                self.is_alive = True
            else:
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
    default_color = GhostColor.RED

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
