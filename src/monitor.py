import pygame

from .parsing import Parser, Config
from .scorer import Scorer
from .pacman_drawer import PacManDrawer
from .entity import Entity, Player, Ghost, Blue, Red, Green, Orange
from .utils import Paths


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.config: Config = Parser(self.config_file).open()
        self.scorer: Scorer = Scorer(self.config.highscore_filename)
        self.entities: list[Entity] = self._init_entities()
        self.maze_index: int = 0

    def _init_entities(self) -> list[Entity]:
        entities = []
        maze = self.config.levels[self.maze_index]
        w = maze.width
        h = maze.height
        ghosts = {Blue, Red, Orange, Green}
        coords = {(0, 0), (0, h), (w, 0), (w, h)}

        center = (maze.width // 2, maze.height // 2)
        entities.append(Player(Paths.PACMAN, center, 60))
        for g, c in zip(ghosts, coords):
            entities.append(Ghost(g, c))
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
