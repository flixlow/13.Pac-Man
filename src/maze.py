
from pydantic import BaseModel


class MazeLevel(BaseModel):
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
