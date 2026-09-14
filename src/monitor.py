import pygame
from random import shuffle
from typing import Callable

from .scorer import Scorer
from .maze import MazeLevel
from .utils import Direction, PlayerState, State
from .parsing import parsing, Config
from .drawing.pacman_drawer import PacManDrawer
from .drawing.basic_drawer import Drawer
from .main_menu import Menu
from .entity import Entity, Ghost, Player, Blue, Red, Green, Orange


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
        self.player_state: PlayerState = PlayerState()
        self.mazes: list[MazeLevel] = self.config.generate_all_maze()
        self.maze_index: int = 0
        self.level: MazeLevel = self.mazes[self.maze_index]

        self._init_entities(self.mazes[self.maze_index])

        self.pygame_info = pygame.display.Info()
        self.screen_size = (
            self.pygame_info.current_w // 2,
            self.pygame_info.current_h // 2
        )
        w, h = self.screen_size
        self.header: int = h // 5
        self.header_img = Drawer((w, h // 5))
        self.header_img.fill((255, 255, 255))

        self.maze_index: int = 0
        self.config_file = config_file
        self.config: Config = parsing(self.config_file)
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.menu = Menu((w, h - self.header))
        self.entities: list[Entity] = self._init_entities()

        self.state = State.MAIN_MENU

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.RESIZABLE
        )

        self.pacman_frame = PacManDrawer((w, h - self.header), self.level)
        self.pacman_frame.draw_maze()

        self.running: bool = True

    def _init_ghosts(self, maze: MazeLevel) -> None:
        ghost_classes: list[Callable] = [Blue, Red, Orange, Green]

        shuffle(ghost_classes)
        for ghost_class, c in zip(ghost_classes, maze.corners):
            self.entities.append(ghost_class(c, maze))

    def _init_player(self, level: MazeLevel) -> None:
        self.player = Player(((level.w // 2 - 1), (level.h // 2 - 1)), level)

        self.entities.append(self.player)

    def _init_pacgums(self, level: MazeLevel) -> None:
        self.pacgums: set[tuple[int, int]] = set()

        for x in range(level.w):
            for y in range(level.h):
                if level.maze[y][x] == 15:
                    continue
                self.pacgums.add((x, y))

    def _init_entities(self, level: MazeLevel) -> None:
        self.entities: list[Entity] = []

        self._init_ghosts(level)
        self._init_player(level)
        self._init_pacgums(level)

    def next_level(self) -> None:
        self.maze_index += 1

    def check_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE:
                    if self.state is State.MAIN_MENU:
                        self.state = State.PACMAN
                elif event.key == pygame.K_n:
                    pass
                    # self.next_level()
                elif event.key in KEY_DIRECTIONS:
                    new_direction = KEY_DIRECTIONS[event.key]
                    if not self.is_there_a_wall_here(new_direction):
                        self.player.direction = new_direction

            if event.type == pygame.VIDEORESIZE:
                w, h = event.size
                self.screen_size = (w, h)
                self.header = h // 5

                if self.state is State.PACMAN:
                    self.pacman_frame.update_size((w, h - self.header))
                    self.pacman_frame.draw_maze()

                if self.state is State.MAIN_MENU:
                    self.menu.frame.update_size((w, h - self.header))
                    self.menu.draw_menu()

                # always need to be updated
                self.header_img.update_size((w, self.header))
                self.header_img.fill((255, 120, 120))

        return True

    def is_there_a_wall_here(self, direction: Direction) -> bool:
        cell = self.level.get_cell_walls(*self.player.coords)
        return bool(cell & direction.value)

    def display_pacgums(self) -> None:
        x = self.config.levels[self.maze_index].width - 1
        y = self.config.levels[self.maze_index].height - 1
        super_pacgums = [(0, 0), (0, y), (x, 0), (x, y)]

        for pacgum in self.pacgums:
            is_super = True if pacgum in super_pacgums else False
            self.pacman_frame.draw_pacgum(pacgum, is_super)

    def display_entities(self, elapsed_time: int) -> None:
        self.pacman_frame.draw_maze()
        self.display_pacgums()

        for entity in self.entities:
            if entity.can_it_move(elapsed_time):
                entity.moving()

            entity.update_animation(elapsed_time)
            if isinstance(entity, Ghost):
                self.pacman_frame.draw_ghost(
                    entity.render_coords(), entity.color
                )
            else:
                self.pacman_frame.draw_pacman(entity.render_coords())

            if isinstance(entity, Player):
                self.pacgums.discard(entity.coords)

    def main_loop(self) -> None:
        self.display_pacgums()

        while self.running:
            elapsed_time = self.clock.tick(60)

            self.running = self.check_events()

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
