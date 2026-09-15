import pygame
from typing import Iterator, Any

from .scorer import Scorer
from .maze import MazeLevel
from .utils import Direction, PlayerState, State
from .parsing import parsing, Config
from .drawing.pacman_drawer import PacManDrawer
from .drawing.basic_drawer import Drawer
from .main_menu import Menu
from .entity import Ghost
from .game import Game


KEY_DIRECTIONS: dict[int, Direction] = {
        pygame.K_UP: Direction.NORTH,
        pygame.K_w: Direction.NORTH,
        pygame.K_RIGHT: Direction.EAST,
        pygame.K_d: Direction.EAST,
        pygame.K_DOWN: Direction.SOUTH,
        pygame.K_s: Direction.SOUTH,
        pygame.K_LEFT: Direction.WEST,
        pygame.K_a: Direction.WEST,
    }


class Monitor:
    def __init__(self, config_file: str) -> None:
        pygame.init()

        self.config: Config = parsing(config_file)
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.mazes: list[MazeLevel] = self.config.generate_all_maze()

        self.level_interator: Iterator = iter(self.mazes)
        self.level: MazeLevel = next(self.level_interator)

        self.pacman: Game = Game(self.config, self.level)
        self.player_state: PlayerState = PlayerState()

        self._init_pygame()

        self.running: bool = True

    def _init_pygame(self) -> None:
        self.pygame_info = pygame.display.Info()
        self.screen_size = (
            self.pygame_info.current_w // 2,
            self.pygame_info.current_h // 2
        )
        w, h = self.screen_size
        self.header: int = h // 5
        self.header_img = Drawer((w, h // 5))
        self.header_img.fill((255, 255, 255))

        self.menu = Menu((w, h - self.header))
        self.state = State.MAIN_MENU

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.RESIZABLE
        )

        self.pacman_frame = PacManDrawer((w, h - self.header), self.level)
        self.pacman_frame.draw_maze()

    def next_level(self) -> None:
        try:
            self.level = next(self.level_interator)
            self.pacman = Game(self.config, self.level)
            w, h = self.screen_size
            self.pacman_frame = PacManDrawer((w, h - self.header), self.level)
            self.pacman_frame.draw_maze()
        except StopIteration:
            pass

    def check_exit(self, event: Any) -> None:
        if event.type == pygame.QUIT:
            self.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

    def check_keydown(self, event: Any) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.state is State.MAIN_MENU:
                    self.state = State.PACMAN

                if self.state is State.PAUSE:
                    if self.player_state.lives > 0:
                        self.state = State.PACMAN

            elif event.key == pygame.K_n:
                if self.state == State.PACMAN:
                    self.next_level()

            elif self.state != State.PAUSE and event.key in KEY_DIRECTIONS:
                self.pacman.change_direction(KEY_DIRECTIONS[event.key])

    def check_resize(self, event: Any) -> None:
        if event.type == pygame.VIDEORESIZE:
            w, h = event.size
            self.screen_size = (w, h)
            self.header = h // 5

            self.pacman_frame.update_size((w, h - self.header))
            self.menu.frame.update_size((w, h - self.header))

            if self.state is State.PACMAN:
                self.pacman_frame.draw_maze()

            if self.state is State.MAIN_MENU:
                self.menu.draw_menu()

            # always need to be updated
            self.header_img.update_size((w, self.header))
            self.header_img.fill((255, 120, 120))

    def check_events(self) -> None:
        for event in pygame.event.get():
            self.check_exit(event)

            self.check_keydown(event)

            self.check_resize(event)

    def enter_your_name(self) -> None:
        pass

    def display_pacgums(self) -> None:
        for pacgum in self.pacman.pacgums:
            is_super = True if pacgum in self.level.corners else False
            self.pacman_frame.draw_pacgum(pacgum, is_super)

    def display_entities(self, elapsed_time: int) -> None:
        for entity in self.pacman.entities:
            entity.update_animation(elapsed_time)

            if isinstance(entity, Ghost):
                self.pacman_frame.draw_ghost(
                    entity.render_coords(), entity.color
                )
            else:
                self.pacman_frame.draw_pacman(entity.render_coords())

    def main_loop(self) -> None:
        while self.running:
            elapsed_time = self.clock.tick(60)

            self.check_events()

            if not self.pacman.moving_entities(elapsed_time):
                self.player_state.lives -= 1
                self.state == State.PAUSE

            self.pacman_frame.draw_maze()
            self.display_pacgums()
            self.display_entities(elapsed_time)

            self.header_img.put_title(
                (
                    self.screen_size[0] // 2 - self.header_img.w_text // 2,
                    self.header_img.h_text // 2)
            )
            # always blit.
            self.screen.blit(self.header_img.surface, (0, 0))

            if self.state is State.PACMAN:
                self.screen.blit(self.pacman_frame.surface, (0, self.header))

            if self.state is State.MAIN_MENU:
                self.screen.blit(self.menu.frame.surface, (0, self.header))

            pygame.display.flip()

        pygame.quit()
