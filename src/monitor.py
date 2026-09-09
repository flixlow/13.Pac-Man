import pygame
from random import shuffle
from typing import Callable

from .scorer import Scorer
from .parsing import Parser, Config
from .pacman_drawer import PacManDrawer
from .entity import Entity, Player, Blue, Red, Green, Orange


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.maze_index: int = 0
        self.config_file = config_file
        self.config: Config = Parser(self.config_file).open()
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.entities: list[Entity] = self._init_entities()

        pygame.init()
        self.pygame_info = pygame.display.Info()
        self.screen_size = (
            self.pygame_info.current_w // 2,
            self.pygame_info.current_h // 2
        )
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.screen_size, pygame.RESIZABLE
        )

        self.running = True

        self.pacman_frame = PacManDrawer((self.screen_size), self.config)
        self.pacman_frame.draw_maze()

    def _init_entities(self) -> list[Entity]:
        entities: list[Entity] = []
        w = self.config.levels[self.maze_index].width
        h = self.config.levels[self.maze_index].height
        ghosts: list[Callable] = [Blue, Red, Orange, Green]
        coords: set[tuple[int, int]] = {(0, 0), (0, h), (w, 0), (w, h)}

        shuffle(ghosts)
        for ghost_class, c in zip(ghosts, coords):
            entities.append(ghost_class(c))

        self.player: Player = Player((w // 2, h // 2))
        entities.append(self.player)

        return entities

    def check_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.coords
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pass
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    pass
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pass

        return True

    def main_loop(self) -> None:
        while self.running:
            self.running = self.check_events()

            self.screen.blit(self.pacman_frame.surface, (0, 0))
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
