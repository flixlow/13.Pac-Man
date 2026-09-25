
from enum import Enum, auto
from pygame import K_UP, K_w, K_RIGHT, K_d, K_DOWN, K_s, K_LEFT, K_a, time


class Timer:
    def __init__(self) -> None:
        self.elapsed_time = 0
        self.total_spend_time = 0
        self.crazy_mode_elapsed_time = 0

    def tick(self, clock: time.Clock) -> None:
        self.elapsed_time = clock.tick(60)
        self.total_spend_time += self.elapsed_time


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
    CRAZY = auto()
    SECRET = auto()


class Direction(Enum):
    START = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class DisplayState(Enum):
    PRESS_SPACE_TO_RESUME = auto()
    ENTER_YOUR_NAME = auto()
    GAME_OVER = auto() # ici
    IN_GAME = auto()
    MENU = auto()


KEY_DIRECTION: dict[int, Direction] = {
        K_UP: Direction.NORTH,
        K_w: Direction.NORTH,
        K_RIGHT: Direction.EAST,
        K_d: Direction.EAST,
        K_DOWN: Direction.SOUTH,
        K_s: Direction.SOUTH,
        K_LEFT: Direction.WEST,
        K_a: Direction.WEST,
    }
