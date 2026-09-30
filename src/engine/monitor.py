import pygame
from typing import Any

from .maze import Maze
from ..scorer import Scorer
from ..main_menu import Menu
from ..color_utils import theme
from ..parsing import parsing, Config
from .game import PacmanGame, GameState
from ..utils import DisplayState, KEY_DIRECTION, Timer
from ..drawing.pacman_drawer import PacManDrawer
from ..drawing.basic_drawer import Drawer, print_life, print_title, print_score, print_timer
from ..drawing.player_name import PlayerName


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.timer: Timer = Timer()

        self.config: Config = parsing(config_file)
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.mazes: list[Maze] = self.config.generate_all_maze()
        self.game: PacmanGame = PacmanGame(self.config, self.mazes, self.timer)

        self._init_pygame()
        self.time: int = 0
        self.running: bool = True
        self.counter_ending_animation: int = 0

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
        self.header_frame.fill(theme.TITLE_BG.value)

        self.menu = Menu((w, h - self.header), self.scorer)
        self.menu.set_screen_origin((0, self.header))
        self.state = DisplayState.MENU

        self.player_frame = PlayerName((w, h - self.header), self.timer)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.RESIZABLE
        )

        self.pacman_frame = PacManDrawer(
            (w, h - self.header), self.game.level.maze, self.timer
        )

    def check_time(self):
        if self.timer.time_is_over():
            self.game.state = GameState.GAME_OVER
            self.state = DisplayState.PRESS_SPACE_TO_RESUME

    def check_exit(self, event: Any) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        if self.state in {DisplayState.MENU, DisplayState.ENTER_YOUR_NAME} and\
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

    def check_alpha(self, event) -> None:
        if self.state != DisplayState.ENTER_YOUR_NAME:
            return None

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
                    self.scorer.save(self.game.player_state, self.game.level.score)
                self.player_frame.clear()
                self.game._init_new_game()

            else:
                self.player_frame.jsp(None)

    def check_keydown(self, event: Any) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state = GameState.PAUSE

            if event.key == pygame.K_t:
                print(self.game.state)
                theme.cycle()

            if event.key == pygame.K_SPACE:

                if self.state == DisplayState.MENU:
                    self.game.state = GameState.IN_GAME

                elif self.state == DisplayState.PRESS_SPACE_TO_RESUME:
                    self.game.state = GameState.IN_GAME

            elif self.state == DisplayState.IN_GAME\
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

            self.header_frame.fill(theme.TITLE_BG.value)

    def check_buttons(self, event: pygame.event) -> None:
        if self.state != DisplayState.MENU:
            return

        pressed = self.menu.check_buttons(event)

        if 0 in pressed:
            if self.state is DisplayState.MENU:
                self.game.state = GameState.IN_GAME

        if 1 in pressed:
            self.menu.clear_leaderboard()
        if 2 in pressed:
            theme.cycle()
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
        self.header_frame.fill(theme.TITLE_BG.value)

        w, h = self.header_frame.size
        title_font = pygame.font.Font("assets/font/title.otf", w // 20)
        font = pygame.font.Font("assets/font/title.otf", w // 40)

        print_title(self.header_frame, title_font)

        print_life(
            self.header_frame, (0, 0),
            self.pacman_frame.alive.get_width(),
            self.game.player_state.lives,
            self.pacman_frame.alive,
            self.pacman_frame.dead
        )

        text_size = print_score(self.header_frame, font, self.game.level.score)

        print_timer(
            self.header_frame, font, text_size, self.timer, self.timer.time_per_game
        )

        self.screen.blit(self.header_frame.surface, (0, 0))

    def display_game(self) -> None:
        level = self.game.level

        self.pacman_frame.draw_maze()

        self.pacman_frame.draw_multiple_pacgums(level.pacgums)

        self.pacman_frame.draw_multiple_pacgums(level.super_pacgums, True)

        self.pacman_frame.draw_entities(level.entities)

        if self.game.state is GameState.HAS_LOSE_A_LIFE:
            self.pacman_frame.press_space_to_restart("Press SPACE to restart...")

        if self.game.state is GameState.HAS_COMPLETED_LEVEL:
            self.pacman_frame.press_space_to_restart("Press SPACE to continue...")

        if self.game.state is GameState.GAME_OVER:
            self.pacman_frame.press_space_to_restart("Game Over")

        self.screen.blit(self.pacman_frame.surface, (0, self.header))

    def display_menu(self) -> None:
        self.menu.draw_menu()

        self.screen.blit(self.menu.frame.surface, (0, self.header))

    def display_enter_your_name(self) -> None:
        self.player_frame.render()
        self.screen.blit(self.player_frame.frame.surface, (0, self.header))

    def display_state(self) -> None:

        self.display_header()

        match self.state:
            case DisplayState.IN_GAME:
                self.display_game()

            case DisplayState.MENU:
                self.display_menu()

            case DisplayState.ENTER_YOUR_NAME:
                self.display_enter_your_name()

        if self.state is DisplayState.PRESS_SPACE_TO_RESUME:
            self.display_game()

        pygame.display.flip()

    def ending_animation(self) -> None:
        if self.game.state\
                in {GameState.HAS_LOSE_A_LIFE, GameState.HAS_COMPLETED_LEVEL}:
            self.counter_ending_animation += self.timer.elapsed_time

        if self.counter_ending_animation >= self.timer.elapsed_time:

            self.pacman_frame.update_maze(self.game.level.maze)

            self.counter_ending_animation = 0

        # Bug de la string vide dans le fichier json
        # if self.game.state\
        #         in {GameState.GAME_OVER, GameState.HAS_BEATEN_THE_GAME}:
        #     self.scorer.save(self.game.player_state, self.game.level.score)

    def check_game_state(self) -> None:
        match self.game.state:

            case GameState.IN_GAME:
                self.state = DisplayState.IN_GAME

            case GameState.START_NEW_GAME | GameState.PAUSE:
                self.state = DisplayState.MENU

            case GameState.HAS_LOSE_A_LIFE | GameState.HAS_COMPLETED_LEVEL:
                self.state = DisplayState.PRESS_SPACE_TO_RESUME

            case GameState.GAME_OVER:
                self.state = DisplayState.GAME_OVER

            case GameState.HAS_BEATEN_THE_GAME:
                self.state = DisplayState.ENTER_YOUR_NAME

            case GameState.DISPLAY:
                ...

    def main_loop(self) -> None:
        while self.running:

            self.timer.tick(self.clock, self.game.state)

            self.game.running()

            self.check_game_state()

            self.check_user_events()

            self.check_time()

            self.display_state()

            self.ending_animation()

        pygame.quit()
