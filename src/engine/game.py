"""Game engine orchestration and lifecycle logic."""

from typing import Iterator

from .maze import Maze
from .level import Level
from ..parsing import Config
from ..utils import Timer, GameState, CheatMode


class GameEngine:
    """Manage the lifecycle of a full game session.

    Args:
        config: Game configuration.
        mazes: Generated mazes for all levels.
        t: Shared timer.
    """

    def __init__(self, config: Config, mazes: list[Maze], t: Timer) -> None:
        """Initialize the engine and create a fresh game.

        Args:
            config: Runtime configuration.
            mazes: List of generated maze levels.
            t: Shared timer instance.
        """
        self.config: Config = config
        self.mazes: list[Maze] = mazes
        self.timer: Timer = t
        self.init_new_game()

    def init_new_game(self) -> None:
        """Reset the score, lives and level iterator for a fresh game."""
        self.score: int = 0
        self.ultra_vision: bool = False
        self.lives: int = self.config.lives
        self.state: GameState = GameState.START_NEW_GAME
        self.maze_interator: Iterator[Maze] = iter(self.mazes)
        self.next_level()

    def next_level(self) -> None:
        """Advance to the next maze level or mark the game as won."""
        try:
            self.level = Level(next(self.maze_interator), self.timer)
        except StopIteration:
            self.state = GameState.HAS_BEATEN_THE_GAME
        else:
            self.timer.new_level()

    def bank_score(self) -> None:
        """Add the points scored from the current level to the global score."""
        self.score += sum(
            count * self.config.points.__getattribute__(item.value)
            for item, count in self.level.eaten.items()
        )
        self.level.eaten.clear()

    def toggle_cheat_mode(self, mode: CheatMode) -> None:
        """Toggle a cheat mode on or off.

        Args:
            mode: Cheat mode to switch.
        """
        match mode:
            case CheatMode.NOCLIP:
                self.level.player.noclip = not self.level.player.noclip

            case CheatMode.ULTRA_VISION:
                self.ultra_vision = not self.ultra_vision

            case CheatMode.GODMODE:
                self.level.on_godmode = not self.level.on_godmode

    def update_game_state(self) -> None:
        """Update the current game state after a tick.

        This resolves game-over, life-lost and level-completed conditions.
        """
        self.bank_score()

        if self.timer.is_over():
            self.state = GameState.GAME_OVER

        if self.level.is_completed:
            self.state = GameState.HAS_COMPLETED_LEVEL
            self.level.set_crazy_mode(False)

        elif not self.level.player.is_alive:
            self.state = GameState.HAS_LOSE_A_LIFE
            self.level.set_crazy_mode(False)
            self.level.player.is_alive = True
            self.lives -= 1

        if self.lives < 1:
            self.state = GameState.GAME_OVER

    def running(self) -> None:
        """Advance the running game one update cycle when state is active."""
        if self.state is GameState.IN_GAME:
            self.level.update()
            self.update_game_state()
