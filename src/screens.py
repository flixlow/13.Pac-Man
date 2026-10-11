from abc import ABC, abstractmethod
from typing import Callable
import pygame

from .menu import Menu
from .scorer import Scorer
from .engine.game import GameEngine
from .theme_selection import ThemeSelection
from .drawing.player_name import PlayerName
from .drawing.pacman_drawer import PacManDrawer
from .utils import KEY_DIRECTION, CheatMode, GameState, Pos


class Screen(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def draw(self, screen: pygame.Surface, pos: Pos) -> None:
        ...


class MenuScreen(Screen):
    def __init__(
            self, game: GameEngine, menu: Menu,
            theme_selection: ThemeSelection, on_quit: Callable[[], None]
            ) -> None:
        self.game = game
        self.menu = menu
        self.theme_selection = theme_selection
        self.on_quit = on_quit

    def button_actions(self, pressed: list[int]) -> None:
        if 0 in pressed:
            self.game.state = GameState.IN_GAME
        if 1 in pressed:
            self.menu.clear_leaderboard()
        if 2 in pressed:
            self.theme_selection.cycle()
        if 3 in pressed:
            self.on_quit()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_quit()

            elif event.key == pygame.K_SPACE:
                self.game.state = GameState.IN_GAME

        self.button_actions(self.menu.check_buttons(event))

    def draw(self, screen: pygame.Surface, pos: Pos) -> None:
        self.menu.draw_menu()

        screen.blit(self.menu.frame.surface, pos)


class GameScreen(Screen):
    CHEATS = {
        pygame.K_F1: CheatMode.ULTRA_VISION,
        pygame.K_F2: CheatMode.GODMODE,
        pygame.K_F3: CheatMode.NOCLIP,
    }

    def __init__(
            self, game: GameEngine,
            theme: ThemeSelection,
            pacman_frame: PacManDrawer
            ) -> None:
        self.game = game
        self.theme_selection = theme
        self.pacman_frame = pacman_frame

    def _space_pressed(self) -> None:
        state = self.game.state

        if state is GameState.HAS_COMPLETED_LEVEL:
            self.theme_selection.cycle()

        if state in {GameState.HAS_LOSE_A_LIFE, GameState.HAS_COMPLETED_LEVEL}:
            self.game.state = GameState.IN_GAME
        elif state in {GameState.GAME_OVER, GameState.HAS_BEATEN_THE_GAME}:
            self.game.state = GameState.ENTER_YOUR_NAME

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        key = event.key

        if key == pygame.K_ESCAPE:
            self.game.state = GameState.PAUSE

        elif key == pygame.K_SPACE:
            self._space_pressed()

        elif key in self.CHEATS:
            self.game.toggle_cheat_mode(self.CHEATS[key])

        elif self.game.state is GameState.IN_GAME and key in KEY_DIRECTION:
            self.game.level.change_direction(KEY_DIRECTION[key])

    def display_state(self) -> None:
        match self.game.state:
            case GameState.HAS_LOSE_A_LIFE:
                self.pacman_frame.press_space("Press SPACE to restart...")
            case GameState.HAS_COMPLETED_LEVEL:
                self.pacman_frame.press_space("Press SPACE to continue...")
            case GameState.GAME_OVER:
                self.pacman_frame.press_space("Game Over.")
            case GameState.HAS_BEATEN_THE_GAME:
                self.pacman_frame.press_space("You finished the Game !")

    def draw_ultra_vision(self) -> None:
        if not self.game.level.on_crazy_mode and self.game.ultra_vision:
            for ghost in self.game.level.ghosts:
                color, sequence = ghost.color, ghost.sequence
                sequence = list(reversed(sequence))
                self.pacman_frame.draw_ghost_path(color, sequence)

    def draw(self, screen: pygame.Surface, pos: Pos) -> None:
        level = self.game.level

        self.pacman_frame.draw_maze()

        self.draw_ultra_vision()

        self.pacman_frame.draw_multiple_pacgums(level.pacgums, False)
        self.pacman_frame.draw_multiple_pacgums(level.super_pacgums, True)
        self.pacman_frame.draw_entities(level.entities)

        self.display_state()

        screen.blit(self.pacman_frame.surface, pos)


class NameScreen(Screen):
    def __init__(
            self, game: GameEngine, player_frame: PlayerName,
            scorer: Scorer, on_new_game: Callable[[], None]
            ) -> None:
        self.game = game
        self.player_frame = player_frame
        self.scorer = scorer
        self.on_new_game = on_new_game

    def _validate(self) -> None:
        name = "".join(self.player_frame.name)
        if not name:
            return
        self.scorer.save(name, self.game.score)
        self.player_frame.clear()
        self.game.init_new_game()
        self.on_new_game()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        key = event.key
        char = event.unicode

        if key == pygame.K_ESCAPE:
            self.game.state = GameState.START_NEW_GAME
            self.game.init_new_game()

        elif key == pygame.K_RETURN:
            self._validate()

        elif key in [
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_BACKSPACE
        ]:
            self.player_frame.handle_player_name_input(event)

        elif char and char.isascii() and char.isalnum():
            self.player_frame.handle_player_name_input(event)

    def draw(self, screen: pygame.Surface, pos: Pos) -> None:
        self.player_frame.render()
        screen.blit(self.player_frame.frame.surface, pos)
