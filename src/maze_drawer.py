import pygame

from .drawer import Frame
from .parsing import Config

"""
class Config(BaseModel):
    highscore_filename: str
    width_and_height: list[list[int]]
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int = Field(gt=0)
    points_per_super_pacgum: int = Field(gt=0)
    points_per_ghost: int = Field(gt=0)
    seeds: list[int]
    level_max_time: int = Field(gt=0)
"""


class MazeDrawer(Frame):
    def __init__(self, size: tuple[int, int], config: Config) -> None:
        self.surface = pygame.Surface(size)
        self.config = config

    def draw_maze(self) -> None:
        pass

    def draw_cell(self, value: int, cell: tuple[int, int]) -> None:
        pass

    def draw_gum(self) -> None:
        pass
