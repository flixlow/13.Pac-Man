
from typing import Iterator

from .maze import Maze
from .level import Level
from ..parsing import Config
from ..utils import PlayerState, State, Timer


class PacmanGame:
    def __init__(self, config: Config, mazes: list[Maze], t: Timer) -> None:
        self.config: Config = config
        self.mazes: list[Maze] = mazes
        self.game_over: bool = False
        self.timer = t

    def new_game(self) -> None:
        self.maze_interator: Iterator = iter(self.mazes)
        self.level: Level = Level(next(self.maze_interator), self.timer)
        self.player_state: PlayerState = PlayerState()

    def next_level(self) -> None:
        try:
            self.level = Level(next(self.maze_interator), self.timer)
        except StopIteration:
            self.new_game()

    def save_level_score(self) -> None:
        self.player_state.score += self.level.score

    def enter_your_name(self) -> None:
        self.player_state.name = "secret pablo ghost"

    def ending_level(self) -> State:
        if self.level.is_completed:
            self.save_level_score()
            self.next_level()

        elif not self.level.player.is_alive:
            self.player_state.lives -= 1
            self.level.player.is_alive = True

        if self.player_state.lives < 1:
            self.save_level_score()
            self.enter_your_name()
            self.new_game()
            return State.MAIN_MENU

        return State.PAUSE

    def running(self) -> None:
        if self.level.player.is_alive or not self.game_over:
            self.level.update()
