import pygame
from typing import Any

from .maze import Maze
from ..scorer import Scorer
from .game import PacmanGame
from ..main_menu import Menu
from ..color_utils import theme
from ..parsing import parsing, Config
from ..utils import State, KEY_DIRECTION, Timer
from ..drawing.pacman_drawer import PacManDrawer
from ..drawing.basic_drawer import Drawer, print_life, print_title


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.timer: Timer = Timer()
        self.config: Config = parsing(config_file)
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.mazes: list[Maze] = self.config.generate_all_maze()
        self.game: PacmanGame = PacmanGame(self.config, self.mazes, self.timer)
        self.game.new_game()

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
        self.header_img = Drawer((w, h // 5))
        self.header_img.fill(theme.TITLE_BG.value)

        self.menu = Menu((w, h - self.header), self.scorer)
        self.menu.set_screen_origin((0, self.header))
        self.state = State.MAIN_MENU

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.RESIZABLE
        )

        self.pacman_frame = PacManDrawer(
            (w, h - self.header), self.game.level.maze, self.timer
        )

    def new_game(self) -> None:
        self.scorer.save(self.game.player_state)
        self.game = PacmanGame(self.config, self.mazes, self.timer)
        self.game.new_game()

    def check_exit(self, event: Any) -> None:
        if event.type == pygame.QUIT:
            self.running = False

    def check_keydown(self, event: Any) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == State.MAIN_MENU:
                    self.running = False
                    return
                self.state = State.MAIN_MENU

            if event.key == pygame.K_SPACE:
                if self.state is State.MAIN_MENU:
                    self.state = State.PACMAN

                if self.state is State.PAUSE:
                    self.game.level._init_entities()
                    self.state = State.PACMAN

            elif self.state != State.PAUSE and event.key in KEY_DIRECTION:
                self.game.level.change_direction(KEY_DIRECTION[event.key])

    def check_buttons(self) -> None:
        pressed = self.menu.check_buttons()

        if 0 in pressed:
            if self.state is State.MAIN_MENU:
                self.state = State.PACMAN
        if 1 in pressed:
            pass
        if 2 in pressed:
            theme.cycle()
        if 3 in pressed:
            self.running = False

    def update_size(self, event: Any) -> None:
        if event.type == pygame.VIDEORESIZE:
            w, h = event.size
            self.screen_size = (w, h)
            self.header = h // 5

            self.pacman_frame.update_size((w, h - self.header))
            self.menu.frame.update_size((w, h - self.header))
            self.menu.update_size()
            self.menu.set_screen_origin((0, self.header))

            self.pacman_frame.draw_maze()

            if self.state is State.MAIN_MENU:
                self.menu.draw_menu()

            self.header_img.update_size((w, self.header))
            self.header_img.fill(theme.TITLE_BG.value)

    def check_events(self) -> None:
        for event in pygame.event.get():
            self.check_exit(event)

            self.check_keydown(event)

            self.update_size(event)

            self.check_buttons()

    def display(self) -> None:

        self.header_img.fill(theme.TITLE_BG.value)

        print_title(self.header_img)

        print_life(
            self.header_img, (0, 0),
            self.pacman_frame.alive.get_width(),
            self.game.player_state.lives,
            self.pacman_frame.alive,
            self.pacman_frame.dead
        )

        self.screen.blit(self.header_img.surface, (0, 0))

        if self.state is State.PACMAN:
            self.pacman_frame.draw_maze()

            super = set(
                pg for pg in self.game.level.pacgums
                if pg in self.game.level.maze.corners
            )
            self.pacman_frame.draw_multiple_pacgums(
                super, super=True)
            self.pacman_frame.draw_multiple_pacgums(
                self.game.level.pacgums - super)

            self.pacman_frame.display_entities(
                self.timer.elapsed_time, self.game.level.entities)
            self.screen.blit(self.pacman_frame.surface, (0, self.header))

        if self.state is State.MAIN_MENU:
            self.menu.draw_menu()
            self.screen.blit(self.menu.frame.surface, (0, self.header))

        pygame.display.flip()

    def ending_animation(self) -> None:
        if not self.game.level.player.is_alive or self.game.level.is_completed:
            self.counter_ending_animation += 1

        if self.counter_ending_animation >= self.timer.elapsed_time:
            self.state = self.game.ending_level()

            self.pacman_frame.update_maze(self.game.level.maze)

            self.counter_ending_animation = 0

    def main_loop(self) -> None:

        while self.running:

            self.timer.tick(self.clock)

            self.check_events()

            if self.game.game_over or self.game.has_beaten_the_game:
                print("ENTER YOUR NAME")

            if self.state is State.PACMAN:
                self.game.running()

            self.ending_animation()
            self.display()

        pygame.quit()
