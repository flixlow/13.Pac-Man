
from .entity import Entity
from ..utils import Direction, Parameters


class Player(Entity):
    direction: Direction = Direction.START
    next_direction: Direction = Direction.START
    default_velocity: int = Parameters.PLAYER_VELOCITY

    def is_wall_here(self, direction: Direction) -> bool:
        cell = self.maze.get_cell_walls(*self.coords)
        return bool(cell & direction.value)

    def can_it_move(self, elapsed_ms: int) -> bool:
        if super().can_it_move(elapsed_ms) and self.is_alive:
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
