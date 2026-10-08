import pygame
from typing import Any

from .maze import Maze
from ..scorer import Scorer
from ..main_menu import Menu
from ..parsing import parsing, Config
from .game import PacmanGame, GameState
from ..color_utils import ThemeSelection
from ..utils import Timer, KEY_DIRECTION
from ..drawing.player_name import PlayerName
from ..drawing.pacman_drawer import PacManDrawer
from ..drawing.basic_drawer import Drawer, print_life, print_title
from ..drawing.basic_drawer import print_score, print_timer, print_theme


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.timer: Timer = Timer()

        self.theme_selection: ThemeSelection = ThemeSelection()
        if not self.theme_selection.load_all_themes():
            raise FileNotFoundError("Theme not found !")

        self.config: Config = parsing(config_file)
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.mazes: list[Maze] = self.config.generate_all_maze()
        self.game: PacmanGame = PacmanGame(self.config, self.mazes, self.timer)

        self._init_pygame()
        self.time: int = 0
        self.running: bool = True
        self.counter_ending_animation: int = 0

    def get_theme(self):
        return self.theme_selection.get_selected()

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
                         self.theme_selection)
        self.menu.set_screen_origin((0, self.header))

        self.player_frame = PlayerName((w, h - self.header), self.timer)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.RESIZABLE
        )

        self.pacman_frame = PacManDrawer(
            (w, h - self.header), self.game.level.maze, self.timer,
            self.theme_selection
        )

    def check_exit(self, event: Any) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        if self.game.state in {GameState.PAUSE, GameState.START_NEW_GAME}:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def check_alpha(self, event: Any) -> None:
        if self.game.state != GameState.ENTER_YOUR_NAME:
            return

        print("ok")

        if event.type == pygame.KEYDOWN:
            if event.unicode == " ":
                return
            if (
                "a" <= event.unicode <= "z" or
                "A" <= event.unicode <= "Z"
            ):
                self.player_frame.jsp(event)

            elif "0" <= event.unicode <= "9":
                self.player_frame.jsp(event)

            elif event.key in [
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_LEFT,
                pygame.K_RIGHT,
                pygame.K_BACKSPACE,
                pygame.K_SPACE
            ]:
                self.player_frame.jsp(event)

            elif event.key is pygame.K_RETURN:
                name = "".join(self.player_frame.name)
                self.game.player_state.name = name
                if name != "":
                    self.scorer.save(
                        self.game.player_state, self.game.level.score
                    )
                self.player_frame.clear()
                self.game._init_new_game()

            else:
                self.player_frame.jsp(None)

    def check_keydown(self, event: Any) -> None:
        if self.game.state is GameState.ENTER_YOUR_NAME:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state = GameState.PAUSE

            if event.key == pygame.K_t:
                print(self.game.state)
                print(self.get_theme())
                self.theme_selection.cycle()
                print(self.get_theme())

            if event.key == pygame.K_SPACE:

                if self.game.state in {
                    GameState.START_NEW_GAME, GameState.HAS_LOSE_A_LIFE,
                    GameState.PAUSE, GameState.HAS_COMPLETED_LEVEL
                }:
                    self.game.state = GameState.IN_GAME

                if self.game.state is GameState.GAME_OVER:
                    self.game.state = GameState.ENTER_YOUR_NAME

            elif self.game.state == GameState.IN_GAME\
                    and event.key in KEY_DIRECTION:
                self.game.level.change_direction(KEY_DIRECTION[event.key])

    def check_resize(self, event: Any) -> None:
        if event.type == pygame.VIDEORESIZE:
            w, h = event.size

            self.screen_size = (w, h)
            self.header = h // 5

            self.pacman_frame.update_size((w, h - self.header))
            self.menu.frame.update_size((w, h - self.header))
            self.menu.update_size()
            self.menu.set_screen_origin((0, self.header))
            self.player_frame.frame.update_size((w, h - self.header))
            self.header_frame.update_size((w, self.header))

            self.header_frame.fill(self.get_theme().header.background)

    def check_buttons(self, event: Any) -> None:
        if self.game.state in {GameState.PAUSE, GameState.START_NEW_GAME}:
            pressed = self.menu.check_buttons(event)

            if 0 in pressed:
                self.game.state = GameState.IN_GAME
            if 1 in pressed:
                self.menu.clear_leaderboard()
            if 2 in pressed:
                self.theme_selection.cycle()
            if 3 in pressed:
                self.running = False

    def check_user_events(self) -> None:
        for event in pygame.event.get():
            self.check_exit(event)

            self.check_alpha(event)

            self.check_keydown(event)

            self.check_resize(event)

            self.check_buttons(event)

    def display_header(self) -> None:
        self.header_frame.fill(self.get_theme().header.background)

        w, h = self.header_frame.size
        title_font = pygame.font.Font("assets/font/title.otf", w // 20)
        font = pygame.font.Font("assets/font/title.otf", w // 40)

        prev = print_title(self.header_frame,
                           title_font, self.get_theme().header.title)
        print_theme(self.header_frame, self.get_theme(), font, prev // 3)

        print_life(
            self.header_frame, (0, 0),
            self.pacman_frame.alive.get_width(),
            self.game.player_state.lives,
            self.pacman_frame.alive,
            self.pacman_frame.dead
        )

        text_size = print_score(
            self.header_frame, font,
            self.game.level.score, self.get_theme().header.score
        )

        print_timer(
            self.header_frame, font, text_size, self.timer,
            self.timer.time_per_game, self.get_theme().header.timer
        )

        self.screen.blit(self.header_frame.surface, (0, 0))

    def display_game(self) -> None:
        level = self.game.level

        self.pacman_frame.draw_maze()

        for ghost in self.game.level.ghosts:
            color, sequence = ghost.color, ghost.sequence
            sequence = list(reversed(sequence))
            self.pacman_frame.draw_ghost_path(color, sequence)

        self.pacman_frame.draw_multiple_pacgums(level.pacgums)

        self.pacman_frame.draw_multiple_pacgums(level.super_pacgums, True)

        self.pacman_frame.draw_entities(level.entities)

        match self.game.state:
            case GameState.HAS_LOSE_A_LIFE:
                self.pacman_frame.press_space("Press SPACE to restart...")

            case GameState.HAS_COMPLETED_LEVEL:
                self.pacman_frame.press_space("Press SPACE to continue...")

            case GameState.GAME_OVER:
                self.pacman_frame.press_space("Game Over")

        self.screen.blit(self.pacman_frame.surface, (0, self.header))

    def display_menu(self) -> None:
        self.menu.draw_menu()

        self.screen.blit(self.menu.frame.surface, (0, self.header))

    def display_enter_your_name(self) -> None:
        self.player_frame.render()
        self.screen.blit(self.player_frame.frame.surface, (0, self.header))

    def display_state(self) -> None:

        self.display_header()

        match self.game.state:
            case GameState.IN_GAME:
                self.display_game()
            case GameState.START_NEW_GAME:
                self.display_menu()
            case GameState.PAUSE:
                self.display_menu()
            case GameState.HAS_LOSE_A_LIFE:
                self.display_game()
            case GameState.HAS_COMPLETED_LEVEL:
                self.display_game()
            case GameState.GAME_OVER:
                self.display_game()
            case GameState.ENTER_YOUR_NAME:
                self.display_enter_your_name()
            case GameState.HAS_BEATEN_THE_GAME:
                self.display_enter_your_name()

        pygame.display.flip()

    def ending_animation(self) -> None:
        if self.game.state\
                in {GameState.HAS_LOSE_A_LIFE, GameState.HAS_COMPLETED_LEVEL}:
            self.counter_ending_animation += self.timer.elapsed_time

        if self.counter_ending_animation >= self.timer.elapsed_time:

            self.pacman_frame.update_maze(self.game.level.maze)

            self.counter_ending_animation = 0

        # if self.game.state\
        #         in {GameState.GAME_OVER, GameState.HAS_BEATEN_THE_GAME}:
        #     self.scorer.save(self.game.player_state, self.game.level.score)

    def main_loop(self) -> None:
        while self.running:

            self.timer.tick(self.clock, self.game.state)

            self.game.running()

            self.check_user_events()

            self.display_state()

            self.ending_animation()
            print(self.game.state)

        pygame.quit()
