"""Shared utility types and constants.

This module centralizes common coordinate aliases, enums, path constants and
timing helpers used throughout the project.
"""

from enum import Enum, auto
from pygame import K_UP, K_w, K_RIGHT, K_d, K_DOWN, K_s, K_LEFT, K_a, time

Pos = tuple[int, int]
Size = tuple[int, int]
Color = tuple[int, int, int]


class Paths:
    """Common file-system paths used by the game assets and resources."""

    ASSETS = "assets/"

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


OPPOSITE = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST
}


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


class Timer:
    """Utility to track elapsed time and level time for the game loop.

    Attributes:
        time_per_game: Maximum duration allowed for a level in milliseconds.
        level_time: Time elapsed in the current level.
        elapsed_time: Time elapsed during the last tick.
        total_spend_time: Cumulative time spent since the timer started.
        crazy_mode_elapsed_time: Time spent in crazy mode.
    """

    def __init__(self, time_per_game: int) -> None:
        """Initialize the timer.

        Args:
            time_per_game: Maximum duration allowed per level in milliseconds.
        """
        self.time_per_game: int = time_per_game

        self.level_time: int = 0
        self.elapsed_time: int = 0
        self.total_spend_time: int = 0
        self.crazy_mode_elapsed_time: int = 0

    def set_time_per_game(self, time_per_game: int) -> None:
        """Update the maximum time allowed for a game level.

        Args:
            time_per_game: New duration allowed for a level, in milliseconds.
        """
        self.time_per_game = time_per_game

    def tick(self, clock: time.Clock, state: GameState) -> None:
        """Advance the timer by one game tick.

        Args:
            clock: The pygame clock used to compute elapsed time.
            state: The current game state. The level timer only advances while
                the game is in progress.

        Returns:
            None: The timer updates its internal counters.
        """
        self.elapsed_time = clock.tick(60)
        self.total_spend_time += self.elapsed_time

        if state is GameState.IN_GAME:
            self.level_time = min(
                self.level_time + self.elapsed_time,
                self.time_per_game
            )

    def new_level(self) -> None:
        """Reset the level timer for the start of a new level."""
        self.level_time = 0

    def is_over(self) -> bool:
        """Check whether the current level time has reached its limit.

        Returns:
            True if the level time is equal to the maximum allowed duration.
        """
        return self.time_per_game == self.level_time


class Parameters:
    """Gameplay tuning values used by the game engine."""

    PLAYER_VELOCITY = 5
    GHOST_VELOCITY = 3
    RESPAWN_TIME = 5000
    BLUE_LEN_SEQ = 30
    RED_LEN_SEQ = 15
    PINK_LEN_SEQ = 5
    SECRET_LEN_SEQ_FOR_TP = 15


class GhostColor(Enum):
    """Colors used to render ghosts in their different states."""

    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    PINK = (255, 127, 127)
    ORANGE = (255, 127, 0)
    CRAZY = (255, 255, 255)
    SECRET = (0, 0, 0)


class DisplayState(Enum):
    """States used for the user interface display."""

    PRESS_SPACE_TO_RESUME = auto()
    ENTER_YOUR_NAME = auto()
    IN_GAME = auto()
    MENU = auto()


class CheatMode(Enum):
    """Available cheat modes in the game."""

    NOCLIP = auto()
    GODMODE = auto()
    ULTRA_VISION = auto()


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
