"""Maze data structure and helper functions.

This module defines the grid model used by the engine and the path logic.
"""

from pydantic import BaseModel

from ..utils import Direction, Pos


class Maze(BaseModel):
    """Maze representation used by the game engine.

    Attributes:
        maze_map: 2D grid storing wall bitmasks for each cell.
        corners: Coordinates of the four maze corners.
        seed: Random seed used to generate the maze.
        w: Maze width in cells.
        h: Maze height in cells.
    """

    maze_map: list[list[int]]
    corners: list[Pos]
    seed: int
    w: int
    h: int

    @property
    def x_max(self) -> int:
        """Return the maximum valid x coordinate."""
        return self.w - 1

    @property
    def y_max(self) -> int:
        """Return the maximum valid y coordinate."""
        return self.h - 1

    def is_in_maze(self, x: int, y: int) -> bool:
        """Check whether a grid position lies inside the maze.

        Args:
            x: Horizontal cell index.
            y: Vertical cell index.

        Returns:
            True if the coordinate is within bounds.
        """
        return 0 <= x < self.w and 0 <= y < self.h

    def get_cell_walls(self, x: int, y: int) -> int:
        """Return wall flags for the given cell.

        Args:
            x: Horizontal coordinate.
            y: Vertical coordinate.

        Returns:
            Bitmask representing walls around the cell.
        """
        if not self.is_in_maze(x, y):
            return False
        return self.maze_map[y][x]

    def get_neighbour_cells(self, pos: Pos, radius: int) -> set[Pos]:
        """Return neighbouring cells within a radius.

        Args:
            pos: Center position.
            radius: Maximum distance used for neighbour selection.

        Returns:
            Set of neighbouring coordinates.
        """
        pos_x, pos_y = pos
        neightbour_cells: set[Pos] = set()

        for x in range(self.w):
            for y in range(self.h):
                if abs(x - pos_x) <= 1 or abs(y - pos_y) <= 1:
                    continue

                if abs(x - pos_x) <= radius or abs(y - pos_y) <= radius:
                    if self.maze_map[y][x] != 15:
                        neightbour_cells.add((x, y))
        return neightbour_cells

    def get_available_coords(self, last_coords: Pos) -> list[Pos]:
        """Return adjacent cells that are not blocked by a wall.

        Args:
            last_coords: Current cell coordinates.

        Returns:
            List of reachable neighboring positions.
        """
        coords: list[Pos] = []
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

    def get_border_cells(self) -> set[Pos]:
        """Return all border cells of the maze.

        Returns:
            Set of coordinates on the outer boundary.
        """
        border_cells: set[Pos] = set()

        for x in range(self.w):
            for y in range(self.h):
                if x in {0, self.x_max} or y in {0, self.y_max}:
                    border_cells.add((x, y))

        return border_cells
