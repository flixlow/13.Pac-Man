"""Screen abstractions and screen-specific event handling.

Each screen owns the game state transitions and rendering logic for the
different parts of the UI.
"""

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
    """Abstract base class for all UI screens."""

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle one pygame event.

        Args:
            event: Event received from the main loop.
        """
        ...

    @abstractmethod
    def draw(self, screen: pygame.Surface, pos: Pos) -> None:
        """Render the screen onto the target surface.

        Args:
            screen: Destination display surface.
            pos: Top-left position where the screen is blitted.
        """
        ...


class MenuScreen(Screen):
    """Main menu screen with buttons and leaderboard panel."""

    def __init__(
            self,
            game: GameEngine,
            menu: Menu,
            theme_selection: ThemeSelection,
            on_quit: Callable[[], None]
            ) -> None:
        """Initialize the menu screen.

        Args:
            game: Active game engine.
            menu: Menu object rendering the UI.
            theme_selection: Theme selection manager.
            on_quit: Callback executed when the user quits.
        """
        self.game = game
        self.menu = menu
        self.theme_selection = theme_selection
        self.on_quit = on_quit

    def button_actions(self, pressed: list[int]) -> None:
        """Execute menu actions for the pressed buttons.

        Args:
            pressed: List of button indexes that were activated.
        """
        if 0 in pressed:
            self.game.state = GameState.IN_GAME
        if 1 in pressed:
            self.menu.clear_leaderboard()
        if 2 in pressed:
            self.theme_selection.cycle()
        if 3 in pressed:
            self.on_quit()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle input events for the menu screen.

        Args:
            event: pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_quit()

            elif event.key == pygame.K_SPACE:
                self.game.state = GameState.IN_GAME

        self.button_actions(self.menu.check_buttons(event))

    def draw(self, screen: pygame.Surface, pos: Pos) -> None:
        """Render the menu screen.

        Args:
            screen: Destination surface.
            pos: Position of the menu frame.
        """
        self.menu.draw_menu()

        screen.blit(self.menu.frame.surface, pos)


class GameScreen(Screen):
    """Gameplay screen that renders the maze, entities and HUD."""

    CHEATS = {
        pygame.K_F1: CheatMode.ULTRA_VISION,
        pygame.K_F2: CheatMode.GODMODE,
        pygame.K_F3: CheatMode.NOCLIP,
    }

    def __init__(
            self,
            game: GameEngine,
            theme: ThemeSelection,
            pacman_frame: PacManDrawer
            ) -> None:
        """Initialize the game screen.

        Args:
            game: active game engine.
            theme: selected theme manager.
            pacman_frame: renderer for the maze and entities.
        """
        self.game = game
        self.theme_selection = theme
        self.pacman_frame = pacman_frame

    def _space_pressed(self) -> None:
        """Handle the space key depending on the current game state."""
        match self.game.state:
            case GameState.HAS_COMPLETED_LEVEL:
                self.game.state = GameState.IN_GAME
                self.game.next_level()
                self.pacman_frame.update_maze(self.game.level.maze)
                self.game.level.init_entities()
                self.theme_selection.cycle()

            case GameState.HAS_LOSE_A_LIFE:
                self.game.state = GameState.IN_GAME
                self.game.level.init_entities()

            case GameState.GAME_OVER | GameState.HAS_BEATEN_THE_GAME:
                self.game.state = GameState.ENTER_YOUR_NAME

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle key input for the gameplay screen.

        Args:
            event: pygame event to process.
        """
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
        """Display contextual overlay text based on the current game state."""
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
        """Render ghost paths when ultra vision cheat mode is active."""
        if not self.game.level.on_crazy_mode and self.game.ultra_vision:
            for ghost in self.game.level.ghosts:
                color, sequence = ghost.color, ghost.sequence
                sequence = list(reversed(sequence))
                self.pacman_frame.draw_ghost_path(color, sequence)

    def draw(self, screen: pygame.Surface, pos: Pos) -> None:
        """Render the game frame and blit it to the main display.

        Args:
            screen: Destination surface.
            pos: Top-left position of the frame.
        """
        level = self.game.level

        self.pacman_frame.draw_maze()

        self.draw_ultra_vision()

        self.pacman_frame.draw_multiple_pacgums(level.pacgums, False)
        self.pacman_frame.draw_multiple_pacgums(level.super_pacgums, True)
        self.pacman_frame.draw_entities(level.entities)

        self.display_state()

        screen.blit(self.pacman_frame.surface, pos)


class NameScreen(Screen):
    """Screen used to enter the player's name after a game session."""

    def __init__(self, game: GameEngine, player_frame: PlayerName,
                 scorer: Scorer, on_new_game: Callable[[], None]) -> None:
        """Initialize the name-entry screen.

        Args:
            game: game engine instance.
            player_frame: name entry renderer.
            scorer: leaderboard persistence object.
            on_new_game: callback used when a new game starts.
        """
        self.game = game
        self.player_frame = player_frame
        self.scorer = scorer
        self.on_new_game = on_new_game

    def _validate(self) -> None:
        """Persist the current score if a non-empty name was entered."""
        name = "".join(self.player_frame.name)
        if not name:
            return

        try:
            self.scorer.save(name, self.game.score)
        except Exception:
            print("[WARNING]: can't save player_name/score to learderboard.")

        self.player_frame.clear()
        self.game.init_new_game()
        self.on_new_game()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle input while the player enters their name.

        Args:
            event: event emitted by pygame.
        """
        if event.type != pygame.KEYDOWN:
            return

        key = event.key
        char = event.unicode

        if key == pygame.K_ESCAPE:
            self.game.init_new_game()
            self.on_new_game()

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
        """Render the name input screen.

        Args:
            screen: destination surface.
            pos: top-left origin for the frame.
        """
        self.player_frame.render()
        screen.blit(self.player_frame.frame.surface, pos)
