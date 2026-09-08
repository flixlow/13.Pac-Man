import sys
import pygame
from pydantic import ValidationError

from .errors import ParsingError, PacmanError
from .parsing import Parser
from .scorer import Scorer
from .pacman_drawer import PacManDrawer
# from .generator import get_maze


def main():
    if len(sys.argv) != 2:
        raise ParsingError(
            "It must take exactly one argument: a configuration file."
        )

    parser = Parser(sys.argv[1])
    config = parser.open()

    scorer = Scorer(config.highscore_filename)
    print(scorer.highscore)

    pygame.init()

    screen = pygame.display.set_mode((2000, 2000))

    first_frame = PacManDrawer((2000, 2000), config)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    running = False

        first_frame.draw_maze()
        screen.blit(first_frame.surface, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except (PacmanError, ValidationError) as e:
        print(f"[ERROR]: {e}")
