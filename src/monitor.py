import pygame
from random import shuffle
from typing import Callable

from .scorer import Scorer
from .utils import Direction
from .parsing import parsing, Config
from .drawing.pacman_drawer import PacManDrawer
from .entity import Entity, Ghost, Player, Blue, Red, Green, Orange


class Monitor:
    def __init__(self, config_file: str) -> None:
        pygame.init()

        self.maze_index: int = 0
        self.config_file = config_file
        self.config: Config = parsing(self.config_file)
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.entities: list[Entity] = self._init_entities()

        self.pygame_info = pygame.display.Info()
        self.screen_size = (
            self.pygame_info.current_w // 2,
            self.pygame_info.current_h // 2
        )
        self.header = self.screen_size[1]//5

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.RESIZABLE
        )

        self.running = True

        w, h = self.screen_size
        self.pacman_frame = PacManDrawer((w, h - self.header), self.config)
        self.pacman_frame.draw_maze()
        self.key_directions: dict[int, Direction] = {
            pygame.K_UP: Direction.NORTH,
            pygame.K_w: Direction.NORTH,
            pygame.K_RIGHT: Direction.EAST,
            pygame.K_d: Direction.EAST,
            pygame.K_DOWN: Direction.SOUTH,
            pygame.K_s: Direction.SOUTH,
            pygame.K_LEFT: Direction.WEST,
            pygame.K_a: Direction.WEST,
        }

    def _init_entities(self) -> list[Entity]:
        entities: list[Entity] = []
        w = self.config.levels[self.maze_index].width
        h = self.config.levels[self.maze_index].height
        ghost_classes: list[Callable] = [Blue, Red, Orange, Green]
        coords = {(0, 0), (0, (h - 1)), ((w - 1), 0), ((w - 1), (h - 1))}

        shuffle(ghost_classes)
        for ghost_class, c in zip(ghost_classes, coords):
            entities.append(ghost_class(c, self.config.mazes[self.maze_index]))

        maze = self.config.mazes[self.maze_index]
        player = Player(((w // 2 - 1), (h // 2 - 1)), maze)
        self.player: Player = player

        entities.append(player)

        self.pacgums: set[tuple[int, int]] = set()
        for x in range(w):
            for y in range(h):
                if self.config.mazes[self.maze_index][y][x] == 15:
                    continue
                self.pacgums.add((x, y))

        return entities

    def next_level(self) -> None:
        self.maze_index += 1

    def check_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_n:
                    pass
                    # self.next_level()
                elif event.key in self.key_directions:
                    new_direction = self.key_directions[event.key]
                    if not self.is_there_a_wall_here(new_direction):
                        self.player.direction = new_direction

            if event.type == pygame.VIDEORESIZE:
                w, h = event.size
                self.pacman_frame.update_size((w, h - h // 10))
                self.pacman_frame.draw_maze()

        return True

    def get_cell_walls(self, coords: tuple[int, int]) -> int:
        x, y = coords
        return self.config.mazes[self.maze_index][y][x]

    def is_there_a_wall_here(self, direction: Direction) -> bool:
        cell = self.get_cell_walls(self.player.coords)
        return bool(cell & direction.value)

    def display_pacgums(self) -> None:
        x = self.config.levels[self.maze_index].width - 1
        y = self.config.levels[self.maze_index].height - 1
        super_pacgums = [(0, 0), (0, y), (x, 0), (x, y)]

        for pacgum in self.pacgums:
            is_super = True if pacgum in super_pacgums else False
            self.pacman_frame.draw_pacgum(pacgum, is_super)

    def display_entities(self, elapsed_time: int) -> None:
        for entity in self.entities:
            if entity.can_it_move(elapsed_time):

                cell = self.get_cell_walls(entity.coords)

                self.pacman_frame.draw_cell(cell, entity.coords, bg=True)

                entity.moving()

                if isinstance(entity, Ghost):
                    self.pacman_frame.draw_ghost(entity.coords, entity.color)
                else:
                    self.pacman_frame.draw_pacman(entity.coords)

                self.pacgums.discard(entity.coords)

    def main_loop(self) -> None:
        self.display_pacgums()

        while self.running:
            elapsed_time = self.clock.tick(60)

            self.running = self.check_events()

            self.display_entities(elapsed_time)

            self.screen.blit(self.pacman_frame.surface, (0, 0))

            pygame.display.flip()

        pygame.quit()
