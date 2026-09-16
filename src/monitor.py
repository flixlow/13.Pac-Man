import pygame
from typing import Iterator, Any

from .scorer import Scorer
from .maze import Maze
from .utils import PlayerState, State, KEY_DIRECTION
from .parsing import parsing, Config
from .drawing.pacman_drawer import PacManDrawer
from .drawing.basic_drawer import Drawer, print_life
from .main_menu import Menu
from .entity import Ghost
from .game import Level


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.config: Config = parsing(config_file)
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.mazes: list[Maze] = self.config.generate_all_maze()
        self.new_game()

        self._init_pygame()
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
        self.header_img.fill((255, 255, 255))

        self.menu = Menu((w, h - self.header), self.scorer)
        self.state = State.MAIN_MENU

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.RESIZABLE
        )

        self.pacman_frame = PacManDrawer((w, h - self.header), self.level)
        self.pacman_frame.draw_maze()

    def new_game(self) -> None:
        self.level_interator: Iterator = iter(self.mazes)
        self.level: Maze = next(self.level_interator)
        self.pacman: Level = Level(self.config, self.level)
        self.player_state: PlayerState = PlayerState()

    def next_level(self) -> None:
        try:
            self.level = next(self.level_interator)
            self.pacman = Level(self.config, self.level)
            w, h = self.screen_size
            self.pacman_frame = PacManDrawer((w, h - self.header), self.level)
            self.pacman_frame.draw_maze()
        except StopIteration:
            self.new_game()

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
                    self.pacman._init_entities()
                    self.state = State.PACMAN

            elif self.state != State.PAUSE and event.key in KEY_DIRECTION:
                self.pacman.change_direction(KEY_DIRECTION[event.key])

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

            self.header_img.update_size((w, self.header))
            self.header_img.fill((255, 120, 120))

    def check_events(self) -> None:
        for event in pygame.event.get():
            self.check_exit(event)

            self.check_keydown(event)

            self.check_resize(event)

    def save_level_score(self) -> None:
        self.player_state.score += self.pacman.score

    def enter_your_name(self) -> None:
        self.player_state.name = str(input("Enter your name :"))
        self.scorer.save(self.player_state)
        self.scorer.sort_scores()

    def display_press_n_for_next_level(self) -> None:
        pass

    def display_pacgums(self) -> None:
        for pacgum in self.pacman.pacgums:
            is_super = True if pacgum in self.level.corners else False
            self.pacman_frame.draw_pacgum(pacgum, is_super)

    def display_entities(self, elapsed_time: int) -> None:
        for entity in self.pacman.entities:
            entity.update_animation(elapsed_time)

            if isinstance(entity, Ghost):
                params = (entity.render_coords(), entity.color)
                self.pacman_frame.draw_ghost(*params)
            else:
                self.pacman_frame.draw_pacman(entity.render_coords())

    def ending_animation(self, elapsed_time: int) -> None:
        if self.counter_ending_animation >= elapsed_time:
            self.state = State.PAUSE
            if self.pacman.game_end:
                self.save_level_score()
                self.display_press_n_for_next_level()
                self.next_level()
            else:
                self.player_state.lives -= 1
                self.pacman.dead = True

            if self.player_state.lives < 1:
                self.save_level_score()
                self.enter_your_name()
                self.new_game()
                self.menu.draw_menu()
                self.state = State.MAIN_MENU

            self.counter_ending_animation = 0

    def blit_all(self) -> None:
        self.header_img.put_title(
            (
                self.screen_size[0] // 2 - self.header_img.w_text // 2,
                self.header_img.h_text // 2)
        )
        # always blit.
        print_life(self.header_img, (0, 0), self.player_state.lives)
        self.screen.blit(self.header_img.surface, (0, 0))

        if self.state is State.PACMAN:
            self.screen.blit(self.pacman_frame.surface, (0, self.header))

        if self.state is State.MAIN_MENU:
            self.screen.blit(self.menu.frame.surface, (0, self.header))

        pygame.display.flip()

    def main_loop(self) -> None:
        while self.running:
            elapsed_time: int = self.clock.tick(60)

            flag = self.pacman.dead or self.pacman.game_end
            if flag:
                self.counter_ending_animation += 1

            self.check_events()

            if not flag and self.state is State.PACMAN:
                self.pacman.moving_entities(elapsed_time)

            self.pacman_frame.draw_maze()
            self.display_pacgums()
            self.display_entities(elapsed_time)

            self.ending_animation(elapsed_time)
            self.blit_all()

        pygame.quit()
