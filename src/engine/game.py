
from typing import Iterator
from enum import Enum, auto

from .maze import Maze
from .level import Level
from ..parsing import Config
from ..utils import PlayerState, Timer


class GameState(Enum):
    START_NEW_GAME = auto()
    IN_GAME = auto()
    PAUSE = auto()
    HAS_LOSE_A_LIFE = auto()
    HAS_COMPLETED_LEVEL = auto()
    GAME_OVER = auto()
    HAS_BEATEN_THE_GAME = auto()


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

    def next_level(self) -> None:
        try:
            self.level = Level(next(self.maze_interator), self.timer)
        except StopIteration:
            self.state = GameState.HAS_BEATEN_THE_GAME

    def save_level_score(self) -> None:
        self.player_state.score += self.level.score

    def update_state(self) -> None:
        if self.level.is_completed:
            self.state = GameState.HAS_COMPLETED_LEVEL
            self.save_level_score()
            self.next_level()
        elif not self.level.player.is_alive:
            self.state = GameState.HAS_LOSE_A_LIFE
            self.level.player.is_alive = True
            self.player_state.lives -= 1
            self.level._init_entities()

        if self.player_state.lives < 1:
            self.state = GameState.GAME_OVER
            self.save_level_score()
        elif self.state is GameState.HAS_BEATEN_THE_GAME:
            self.save_level_score()

    def running(self) -> None:
        if self.state is GameState.IN_GAME:
            self.level.update()
        self.update_state()
