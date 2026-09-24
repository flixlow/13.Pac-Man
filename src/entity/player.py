
from .entity import Entity
from ..utils import Direction, Parameters


class Player(Entity):
    direction: Direction = Direction.START
    next_direction: Direction = Direction.START
    default_velocity: int = Parameters.PLAYER_VELOCITY

    def get_direction(self) -> Direction:
        return self.direction

    def is_wall_here(self, direction: Direction) -> bool:
        cell = self.maze.get_cell_walls(*self.coords)
        return bool(cell & direction.value)

    def reverse(self, new_direction: Direction) -> None:
        progress = min(
            self.animation_elapsed_ms / max(1, self.movement_interval_ms), 1.0
        )

        self.previous_coords, self.coords = self.coords, self.previous_coords
        self.animation_elapsed_ms = int(
            self.movement_interval_ms * (1 - progress)
        )

        self.entity_move_elapsed_ms = self.animation_elapsed_ms

        self.direction = new_direction
        self.next_direction = Direction.START

    def can_it_move(self) -> bool:
        if not self.is_alive or not super().can_it_move():
            return False

        if (self.next_direction is not Direction.START
                and not self.is_wall_here(self.next_direction)):
            self.direction = self.next_direction
            self.next_direction = Direction.START
            return True

        return not self.is_wall_here(self.direction)

    def moving(self) -> None:
        if not self.can_it_move():
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
