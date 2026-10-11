import pygame

from .maze import Maze
from ..menu import Menu
from ..scorer import Scorer
from .game import GameEngine
from ..utils import Timer, GameState
from ..parsing import parsing, Config
from ..drawing.player_name import PlayerName
from ..drawing.pacman_drawer import PacManDrawer
from ..theme_selection import ThemeSelection, Theme
from .screens import Screen, GameScreen, MenuScreen, NameScreen
from ..drawing.basic_drawer import Drawer, print_life, print_title
from ..drawing.basic_drawer import print_score, print_timer, print_theme


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.config: Config = parsing(config_file)
        self.timer: Timer = Timer(self.config.level_max_time)
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.mazes: list[Maze] = self.config.generate_all_maze()
        self.game: GameEngine = GameEngine(self.config, self.mazes, self.timer)

        self.theme: ThemeSelection = ThemeSelection()
        if not self.theme.load_all_themes():
            raise FileNotFoundError("Theme not found !")

        self._init_pygame()
        self.running: bool = True
        self.counter_ending_animation: int = 0
        self._init_screens()

    def _init_pygame(self) -> None:
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
        menu = MenuScreen(self.game, self.menu, self.theme, self.quit)
        game = GameScreen(self.game, self.theme, self.pacman_frame)
        name = NameScreen(self.game, self.player_frame, self.scorer,
                          self.reset_maze)

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

    def reset_maze(self) -> None:
        self.pacman_frame.update_maze(self.game.level.maze)

    def get_theme(self) -> Theme:
        return self.theme.get_selected()

    def quit(self) -> None:
        self.running = False

    def resize(self, w, h) -> None:
        self.screen_size = (w, h)
        self.header = h // 5

        self.pacman_frame.update_size((w, h - self.header))
        self.menu.frame.update_size((w, h - self.header))
        self.menu.update_size()
        self.menu.set_screen_origin((0, self.header))
        self.player_frame.frame.update_size((w, h - self.header))
        self.header_frame.update_size((w, self.header))
        self.header_frame.fill(self.get_theme().header.background)

    def display_header(self) -> None:
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

        print_life(
            self.header_frame, (0, 0),
            self.pacman_frame.alive.get_width(),
            self.game.lives,
            icons,
            self.get_theme().header.heart_color
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

    def check_user_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.VIDEORESIZE:
                self.resize(*event.size)

            self.screens[self.game.state].handle_event(event)

    def display(self) -> None:
        self.display_header()

        self.screens[self.game.state].draw(self.screen, (0, self.header))

        pygame.display.flip()

    def ending_animation(self) -> None:
        if self.game.state in {
            GameState.HAS_LOSE_A_LIFE,
            GameState.HAS_COMPLETED_LEVEL
        }:
            self.counter_ending_animation += self.timer.elapsed_time

        if self.counter_ending_animation >= self.timer.elapsed_time:
            self.pacman_frame.update_maze(self.game.level.maze)
            self.counter_ending_animation = 0

    def main_loop(self) -> None:
        while self.running:

            self.timer.tick(self.clock, self.game.state)

            self.game.running()

            self.check_user_events()

            self.display()

            self.ending_animation()

        pygame.quit()
