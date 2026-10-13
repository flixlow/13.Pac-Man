"""Shared utility types and constants.

This module centralizes common coordinate aliases, enums, path constants and
timing helpers used throughout the project.
"""

from enum import Enum, auto
from pygame import K_UP, K_w, K_RIGHT, K_d, K_DOWN, K_s, K_LEFT, K_a

Pos = tuple[int, int]
Size = tuple[int, int]
Color = tuple[int, int, int]


class Paths:
    """Common file-system paths used by the game assets and resources."""

    ASSETS = "assets/"

    DEFAULT_CONFIG = ASSETS + "default_config.jsonc"

    BUTTON = ASSETS + "button/"
    UNPRESSED = BUTTON + "button.png"
    PRESSED = BUTTON + "button_pressed.png"

    DEFAULT_THEMES = ASSETS + "default_themes/"
    THEMES = "themes/"

    FONT = ASSETS + "font/"
    LEADERBOARD = FONT + "leaderboard.ttf"
    TITLE = FONT + "title.otf"

    FRUIT = ASSETS + "fruit/"

    ICON = ASSETS + "icon/"
    ALIVE = ICON + "heart.png"
    DEAD = ICON + "dead_heart.png"
    REFLECT = ICON + "reflect.png"

    GHOSTS = ASSETS + "ghosts/"
    RED = GHOSTS + "red/"
    BLUE = GHOSTS + "blue/"
    PINK = GHOSTS + "pink/"
    ORANGE = GHOSTS + "orange/"
    SECRET = GHOSTS + "secret/"
    CRAZY = GHOSTS + "crazyman/"

    CHEAT_ICONS = ASSETS + "cheat_icons/"
    GODMODE = CHEAT_ICONS + "godmode.png"
    NOCLIP = CHEAT_ICONS + "noclip.png"
    ULTRA_VISION = CHEAT_ICONS + "ultra_vision.png"

    PACMAN = ASSETS + "pacman/"


class Direction(Enum):
    """Possible movement directions for entities in the maze.

    Attributes:
        START: Initial state before any direction is chosen.
        NORTH: Movement upward.
        EAST: Movement to the right.
        SOUTH: Movement downward.
        WEST: Movement to the left.
    """

    START = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class TypeScore(Enum):
    """Type of collectible used when computing score gains.

    Attributes:
        GHOST: Score for eating a ghost.
        PACGUM: Score for collecting a regular pacgum.
        SUPER_PACGUM: Score for collecting a super pacgum.
    """

    GHOST = "per_ghost"
    PACGUM = "per_pacgum"
    SUPER_PACGUM = "per_super_pacgum"


class GameState(Enum):
    """States that describe the flow of a game session."""

    START_NEW_GAME = auto()
    IN_GAME = auto()
    PAUSE = auto()
    HAS_LOSE_A_LIFE = auto()
    HAS_COMPLETED_LEVEL = auto()
    GAME_OVER = auto()
    HAS_BEATEN_THE_GAME = auto()
    ENTER_YOUR_NAME = auto()


class Parameters:
    """Gameplay tuning values used by the game engine."""

    PLAYER_VELOCITY = 5
    GHOST_VELOCITY = 3
    RESPAWN_TIME = 5000
    BLUE_LEN_SEQ = 30
    RED_LEN_SEQ = 15
    PINK_LEN_SEQ = 5
    SECRET_SPAWN_CHANCE = 0.1
    SECRET_LEN_SEQ_FOR_TP = 15


class GhostColor(Enum):
    """Colors used to render ghosts in their different states."""

    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    PINK = (255, 127, 127)
    ORANGE = (255, 127, 0)
    CRAZY = (255, 255, 255)
    SECRET = (0, 0, 0)


class CheatMode(Enum):
    """Available cheat modes in the game."""

    NOCLIP = auto()
    GODMODE = auto()
    ULTRA_VISION = auto()
    NEXT = auto()


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

OPPOSITE = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST
}
