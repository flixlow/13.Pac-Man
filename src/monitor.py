import pygame
from typing import Any

from .scorer import Scorer
from .maze import Maze
from .utils import State, KEY_DIRECTION
from .parsing import parsing, Config
from .drawing.pacman_drawer import PacManDrawer
from .drawing.basic_drawer import Drawer, print_life
from .main_menu import Menu
from .entity import Ghost
from .game import PacmanGame


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.config: Config = parsing(config_file)
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.mazes: list[Maze] = self.config.generate_all_maze()
        self.game: PacmanGame = PacmanGame(self.config, self.mazes)
        self.game.new_game()

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

        maze = self.game.maze
        self.pacman_frame = PacManDrawer((w, h - self.header), maze)
        self.pacman_frame.draw_maze()

    def new_game(self) -> None:
        self.scorer.save(self.game.player_state)

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
                    self.game.level._init_entities()
                    self.state = State.PACMAN

            elif self.state != State.PAUSE and event.key in KEY_DIRECTION:
                self.game.level.change_direction(KEY_DIRECTION[event.key])

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

    def display_pacgums(self) -> None:
        for pacgum in self.game.level.pacgums:
            is_super = pacgum in self.game.level.maze.corners
            self.pacman_frame.draw_pacgum(pacgum, is_super)

    def display_entities(self, elapsed_time: int) -> None:
        for entity in self.game.level.entities:
            entity.update_animation(elapsed_time)

            if isinstance(entity, Ghost):
                params = (entity.render_coords(), entity.color)
                self.pacman_frame.draw_ghost(*params)
            else:
                self.pacman_frame.draw_pacman(entity.render_coords())

    def ending_animation(self, elapsed_time: int) -> None:
        if self.game.level.is_dead or self.game.level.is_completed:
            self.counter_ending_animation += 1
        if self.counter_ending_animation >= elapsed_time:
            self.state = self.game.lose_a_life()

            self.counter_ending_animation = 0

    def blit_all(self, elapsed_time: int) -> None:
        self.header_img.put_title(
            (
                self.screen_size[0] // 2 - self.header_img.w_text // 2,
                self.header_img.h_text // 2)
        )
        # always blit.
        print_life(self.header_img, (0, 0), self.game.player_state.lives)
        self.screen.blit(self.header_img.surface, (0, 0))

        if self.state is State.PACMAN:
            self.display_pacgums()
            self.display_entities(elapsed_time)
            self.screen.blit(self.pacman_frame.surface, (0, self.header))

        if self.state is State.MAIN_MENU:
            self.screen.blit(self.menu.frame.surface, (0, self.header))

        pygame.display.flip()

    def main_loop(self) -> None:
        while self.running:
            elapsed_time: int = self.clock.tick(60)

            self.check_events()

            if self.state is State.PACMAN:
                self.game.moving_entities(elapsed_time)

            pos = self.game.level.player.previous_coords
            self.pacman_frame.draw_cell(
                self.game.level.maze.get_cell_walls(*pos),
                pos, bg=True
            )

            self.ending_animation(elapsed_time)
            self.blit_all(elapsed_time)

        pygame.quit()
