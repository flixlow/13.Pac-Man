import pygame

from .drawer import Frame
# from .maze_drawer import MazeDrawer
# from .generator import get_maze


def main():
    print("Hello from 13-pac-man!")

    pygame.init()

    screen = pygame.display.set_mode((1000, 1000))

    first_frame = Frame((500, 500))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        first_frame.fill((0, 255, 0))
        screen.blit(first_frame.surface, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
