
from pydantic import BaseModel

from ..utils import Direction


class Maze(BaseModel):
    maze_map: list[list[int]]
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
        return self.maze_map[y][x]

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

    def get_border_cells(self) -> list[tuple[int, int]]:
        border_cells: list[tuple[int, int]] = []

        for x in range(self.w):
            for y in range(self.h):
                if x in {0, self.x_max} or y in {0, self.y_max}:
                    border_cells.append((x, y))

        return border_cells
