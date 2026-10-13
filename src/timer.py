
from pygame import time

from .utils import GameState


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
