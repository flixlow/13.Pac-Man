
import pygame
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
    PLAYER_VELOCITY = 5
    GHOST_VELOCITY = 3


class PlayerState:
    lives: int = 3
    score: int = 0
    name: str = ""


class GhostColor(Enum):
    RED = auto()
    BLUE = auto()
    PINK = auto()
    ORANGE = auto()
    SECRET = auto()


class Direction(Enum):
    START = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class State(Enum):
    MAIN_MENU = auto()
    PACMAN = auto()
    PAUSE = auto()
    SCORE = auto()
    NEXT = auto()


KEY_DIRECTION: dict[int, Direction] = {
        pygame.K_UP: Direction.NORTH,
        pygame.K_w: Direction.NORTH,
        pygame.K_RIGHT: Direction.EAST,
        pygame.K_d: Direction.EAST,
        pygame.K_DOWN: Direction.SOUTH,
        pygame.K_s: Direction.SOUTH,
        pygame.K_LEFT: Direction.WEST,
        pygame.K_a: Direction.WEST,
    }
