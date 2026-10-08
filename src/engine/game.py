
from typing import Iterator

from .maze import Maze
from .level import Level
from ..parsing import Config
from ..utils import PlayerState, Timer, GameState


class PacmanGame:
    def __init__(self, config: Config, mazes: list[Maze], t: Timer) -> None:
        self.config: Config = config
        self.mazes: list[Maze] = mazes
        self.timer = t
        self._init_new_game()

    def _init_new_game(self) -> None:
        self.player_state: PlayerState = PlayerState()
        self.state: GameState = GameState.START_NEW_GAME
        self.maze_interator: Iterator = iter(self.mazes)
        self.level: Level = Level(next(self.maze_interator), self.timer)
        self.timer.new_game()

    def next_level(self) -> None:
        try:
            self.level = Level(next(self.maze_interator), self.timer)
        except StopIteration:
            self.state = GameState.HAS_BEATEN_THE_GAME
        else:
            self.timer.new_game()

    def save_level_score(self) -> None:
        self.player_state.score = self.level.score

    def update_state(self) -> None:
        if self.timer.is_over():
            self.state = GameState.GAME_OVER
        if self.level.is_completed:
            self.state = GameState.HAS_COMPLETED_LEVEL
            self.next_level()
            self.level.set_crazy_mode(False)
        elif not self.level.player.is_alive:
            self.state = GameState.HAS_LOSE_A_LIFE
            self.level.player.is_alive = True
            self.player_state.lives -= 1
            self.level._init_entities()

        if self.player_state.lives < 1:
            self.state = GameState.GAME_OVER

    def running(self) -> None:
        if self.state is GameState.IN_GAME:
            self.level.update()
            self.update_state()
