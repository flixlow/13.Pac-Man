
from pydantic import BaseModel

from ..utils import Direction


class Maze(BaseModel):
    maze: list[list[int]]
    corners: list[tuple[int, int]]
    seed: int
    w: int
    h: int

    @property
    def x_max(self) -> int:
        return self.w - 1

    @property
    def y_max(self) -> int:
        return self.h - 1

    def get_cell_walls(self, x: int, y: int) -> int:
        return self.maze[y][x]

    def get_available_coords(
            self, last_coords: tuple[int, int]) -> list[tuple[int, int]]:
        coords: list[tuple[int, int]] = []
        x, y = last_coords

        cell = self.get_cell_walls(*last_coords)
        if not cell & Direction.NORTH.value:
            coords.append((x, y - 1))
        if not cell & Direction.EAST.value:
            coords.append((x + 1, y))
        if not cell & Direction.SOUTH.value:
            coords.append((x, y + 1))
        if not cell & Direction.WEST.value:
            coords.append((x - 1, y))

        return coords
