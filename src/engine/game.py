
from typing import Iterator

from .maze import Maze
from ..utils import PlayerState, State
from ..parsing import Config
from .level import Level


class PacmanGame:
    def __init__(self, config: Config, mazes: list[Maze]) -> None:
        self.config: Config = config
        self.mazes: list[Maze] = mazes
        self.game_over: bool = False

    def new_game(self) -> None:
        self.maze_interator: Iterator = iter(self.mazes)
        self.maze: Maze = next(self.maze_interator)
        self.level: Level = Level(self.maze)
        self.player_state: PlayerState = PlayerState()

    def next_level(self) -> None:
        try:
            self.maze = next(self.maze_interator)
            self.level = Level(self.maze)
        except StopIteration:
            self.new_game()

    def moving_entities(self, elapsed_time: int) -> bool:
        if not (self.level.is_dead or self.game_over):
            self.level.moving_entities(elapsed_time)
        if self.level.is_completed:
            return True
        return False

    def save_level_score(self) -> None:
        self.player_state.score += self.level.score

    def enter_your_name(self) -> None:
        self.player_state.name = "secret pablo ghost"

    def lose_a_life(self) -> State:
        if self.level.is_completed:
            self.save_level_score()
            self.next_level()

        elif self.level.is_dead:
            self.player_state.lives -= 1
            self.level.is_dead = False

        if self.player_state.lives < 1:
            self.save_level_score()
            self.enter_your_name()
            self.new_game()
            return State.MAIN_MENU
        return State.PAUSE
