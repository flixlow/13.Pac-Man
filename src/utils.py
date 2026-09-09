
from enum import Enum, auto


class Paths:
    ASSETS = "assets/"
    GHOSTS = ASSETS + "ghosts/"
    PACMAN = ASSETS + "pacman/pacman.png"
    SECRET = GHOSTS + "secret_ghost.png"
    ORANGE = GHOSTS + "orange_ghost.png"
    GREEN = GHOSTS + "green_ghost.png"
    BLUE = GHOSTS + "blue_ghost.png"
    RED = GHOSTS + "red_ghost.png"


class Parameters:
    PLAYER_VELOCITY = 60
    GHOST_VELOCITY = 60


class GhostColor(Enum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    ORANGE = auto()
    SECRET = auto()


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
