
from pydantic import BaseModel


class MazeLevel(BaseModel):
    maze: list[list[int]]
    corners: list[tuple[int, int]]
    seed: int
    w: int
    h: int

    def get_cell_walls(self, x: int, y: int) -> int:
        return self.maze[y][x]
