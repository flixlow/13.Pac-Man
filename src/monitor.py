import pygame
from typing import Callable

from .parsing import Parser, Config
from .scorer import Scorer
from .pacman_drawer import PacManDrawer
from .entity import Entity, Player, Blue, Red, Green, Orange


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.maze_index: int = 0
        self.config_file = config_file
        self.config: Config = Parser(self.config_file).open()
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.entities: list[Entity] = self._init_entities()

    def _init_entities(self) -> list[Entity]:
        entities: list[Entity] = []
        w = self.config.levels[self.maze_index].width
        h = self.config.levels[self.maze_index].height
        ghosts: set[Callable] = {Blue, Red, Orange, Green}
        coords: set[tuple[int, int]] = {(0, 0), (0, h), (w, 0), (w, h)}
        center = (w // 2, h // 2)

        entities.append(Player(center))
        for ghost_class, c in zip(ghosts, coords):
            entities.append(ghost_class(c))

        return entities

    def check_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def main_loop(self) -> None:

        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)
        first_frame = PacManDrawer((500, 500), self.config)
        first_frame.draw_maze()

        running = True

        while running:
            running = self.check_events()

            screen.blit(first_frame.surface, (0, 0))
            pygame.display.flip()

            clock.tick(60)

        pygame.quit()
