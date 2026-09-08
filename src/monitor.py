import pygame

from .parsing import Parser
from .scorer import Scorer
from .pacman_drawer import PacManDrawer


class Monitor:
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.config = Parser(self.config_file).open()
        self.scorer = Scorer(self.config.highscore_filename)

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
        screen = pygame.display.set_mode((2000, 2000))
        first_frame = PacManDrawer((2000, 2000), self.config)
        first_frame.draw_maze()

        running = True

        while running:
            running = self.check_events()

            screen.blit(first_frame.surface, (0, 0))
            pygame.display.flip()

            clock.tick(60)

        pygame.quit()
