
from .entity import Entity
from ..utils import Direction, Parameters


offsets = {
        Direction.NORTH: (0, -1),
        Direction.EAST: (1, 0),
        Direction.SOUTH: (0, 1),
        Direction.WEST: (-1, 0),
        Direction.START: (0, 0),
    }


class Player(Entity):
    noclip: bool = False
    direction: Direction = Direction.START
    next_direction: Direction = Direction.START
    default_velocity: int = Parameters.PLAYER_VELOCITY

    def is_wall_here(self, direction: Direction) -> bool:
        cell = self.maze.get_cell_walls(*self.coords)
        return bool(cell & direction.value)

    def reverse(self, new_direction: Direction) -> None:

        self.previous_coords, self.coords = self.coords, self.previous_coords
        self.animation_elapsed_ms = int(
            self.movement_interval_ms * (1 - self.progress)
        )

        self.entity_move_elapsed_ms = self.animation_elapsed_ms

        self.direction = new_direction
        self.next_direction = Direction.START

    def can_it_move(self) -> bool:
        if not self.is_alive or not super().can_it_move():
            return False

        if self.next_direction is not Direction.START:
            if not self.is_wall_here(self.next_direction):
                self.direction = self.next_direction
                self.next_direction = Direction.START
                return True

        return not self.is_wall_here(self.direction)

    def moving(self) -> None:
        if not self.can_it_move():
            return
        x, y = self.coords
        dx, dy = offsets[self.direction]
        self.previous_coords = self.coords
        self.animation_elapsed_ms = 0
        self.coords = x + dx, y + dy

    def moving_on_noclip(self) -> None:
        if not self.is_alive or not super().can_it_move():
            return

        if self.next_direction is not Direction.START:
            self.direction = self.next_direction
            self.next_direction = Direction.START

        x, y = self.coords
        dx, dy = offsets[self.direction]
        next_pos = x + dx, y + dy

        if not self.maze.is_in_maze(*next_pos):
            return
        if self.maze.get_cell_walls(*next_pos) == 15:
            return

        self.previous_coords = self.coords
        self.animation_elapsed_ms = 0
        self.coords = next_pos
