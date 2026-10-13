"""Controller for the main game loop and screen management.

This module initializes the game configuration, loads themes, creates the
different screens and coordinates rendering and user interaction for the
Pac-Man game.
"""

import pygame

from .menu import Menu
from .timer import Timer
from .scorer import Scorer
from .engine.maze import Maze
from .errors import PacmanError
from .utils import GameState, Paths
from .engine.game import GameEngine
from .parsing import parsing, Config
from .drawing.player_name import PlayerName
from .drawing.pacman_drawer import PacManDrawer
from .theme_selection import ThemeSelection, Theme
from .screens import Screen, GameScreen, MenuScreen, NameScreen
from .drawing.basic_drawer import Drawer, print_life, print_title, print_cheat
from .drawing.basic_drawer import print_score, print_timer, print_theme


class Monitor:
    """Main runtime controller for the game window and states.

    This class initializes the game configuration, manages the user interface,
    updates the display and drives the main loop.
    """

    def __init__(self, config_file: str) -> None:
        """Initialize the monitor with a configuration file.

        Args:
            config_file: Path to the JSON configuration file used to set up the
                game.
        """
        self.running: bool = True
        self.counter_ending_animation: int = 0

        self.config: Config = self._load_config(config_file)
        self.mazes: list[Maze] = self.config.generate_all_maze()

        self.theme: ThemeSelection = ThemeSelection()
        self.timer: Timer = Timer(self.config.level_max_time)
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.game: GameEngine = GameEngine(self.config, self.mazes, self.timer)

        self._init_pygame()
        self._init_screens()

    def _load_config(self, config_file: str) -> Config:
        try:
            return parsing(config_file)
        except (PacmanError, Exception, KeyboardInterrupt) as e:
            print(f"[WARNING] {e.__class__.__name__}: {e}")
            print("[ON] default config file.")
            return parsing(Paths.DEFAULT_CONFIG)

    def _init_pygame(self) -> None:
        """Initialize pygame resources and the main display components."""
        pygame.init()
        self.pygame_info = pygame.display.Info()
        self.screen_size = (
            self.pygame_info.current_w // 2,
            self.pygame_info.current_h // 2
        )
        w, h = self.screen_size
        self.header: int = h // 5
        self.header_frame = Drawer((w, h // 5))
        self.header_frame.fill(self.get_theme().header.background)

        self.menu = Menu((w, h - self.header), self.scorer,
                         self.theme)
        self.menu.set_screen_origin((0, self.header))

        self.player_frame = PlayerName((w, h - self.header), self.timer)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.RESIZABLE
        )

        self.pacman_frame = PacManDrawer(
            (w, h - self.header), self.game.level.maze, self.timer,
            self.theme
        )

    def _init_screens(self) -> None:
        """Create the screen objects used for each game state."""
        menu = MenuScreen(self.game, self.menu, self.theme, self.quit)
        game = GameScreen(self.game, self.theme, self.pacman_frame)
        name = NameScreen(self.game, self.player_frame, self.scorer,
                          self.on_new_game)

        self.screens: dict[GameState, Screen] = {
            GameState.START_NEW_GAME: menu,
            GameState.PAUSE: menu,
            GameState.IN_GAME: game,
            GameState.HAS_LOSE_A_LIFE: game,
            GameState.HAS_COMPLETED_LEVEL: game,
            GameState.GAME_OVER: game,
            GameState.HAS_BEATEN_THE_GAME: game,
            GameState.ENTER_YOUR_NAME: name,
        }

    def on_new_game(self) -> None:
        """Refresh the displayed maze after a reset or game state change."""
        self.game.init_new_game()
        self.theme.selected_index = 0
        self.pacman_frame.update_maze(self.game.level.maze)

    def get_theme(self) -> Theme:
        """Get the currently selected theme.

        Returns:
            The active theme configuration.
        """
        return self.theme.get_selected()

    def quit(self) -> None:
        """Stop the main loop and close the application."""
        self.running = False

    def resize(self, w: int, h: int) -> None:
        """Resize the game window and all dependent frames.

        Args:
            w: New width of the window.
            h: New height of the window.
        """
        self.screen_size = (w, h)
        self.header = h // 5

        self.pacman_frame.update_size((w, h - self.header))
        self.menu.frame.update_size((w, h - self.header))
        self.menu.update_size()
        self.menu.set_screen_origin((0, self.header))
        self.player_frame.frame.update_size((w, h - self.header))
        self.header_frame.update_size((w, self.header))
        self.header_frame.fill(self.get_theme().header.background)

    def check_user_events(self) -> None:
        """Handle pygame events and forward them to the active screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.VIDEORESIZE:
                self.resize(*event.size)

            self.screens[self.game.state].handle_event(event)

    def display_header(self) -> None:
        """Render the header bar with the title, theme, score and timer."""
        self.header_frame.fill(self.get_theme().header.background)

        w, h = self.header_frame.size
        title_font = pygame.font.Font("assets/font/title.otf", w // 20)
        font = pygame.font.Font("assets/font/title.otf", w // 40)

        prev = print_title(self.header_frame,
                           title_font, self.get_theme().header.title)
        print_theme(self.header_frame, self.get_theme(), font, prev // 3)

        icons = (
            self.pacman_frame.alive,
            self.pacman_frame.dead,
            self.pacman_frame.reflect
        )

        offset_y = print_life(
            self.header_frame, (0, 0),
            self.pacman_frame.alive.get_width(),
            self.game.lives,
            icons,
            self.get_theme().header.heart_color
        )

        print_cheat(
            self.header_frame, offset_y, self.game.level.on_godmode,
            self.game.level.player.noclip, self.game.ultra_vision
        )

        text_size = print_score(
            self.header_frame, font,
            self.game.score, self.get_theme().header.score
        )

        print_timer(
            self.header_frame, font, text_size, self.timer,
            self.timer.time_per_game, self.get_theme().header.timer
        )

        self.screen.blit(self.header_frame.surface, (0, 0))

    def display(self) -> None:
        """Draw the current screen and the header to the main display."""
        self.display_header()

        self.screens[self.game.state].draw(self.screen, (0, self.header))

        pygame.display.flip()

    def main_loop(self) -> None:
        """Run the main application loop."""
        while self.running:

            self.timer.tick(self.clock, self.game.state)

            self.game.running()

            self.check_user_events()

            self.display()

        pygame.quit()
