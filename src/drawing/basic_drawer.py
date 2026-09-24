import pygame

from ..color_utils import theme


class Drawer:
    def __init__(self, size: tuple[int, int]) -> None:
        """
        Initialise the Frame

        Args:
            size (tuple[int, int]) dimensions of the frame
        """
        self.size = size

        self.surface = pygame.Surface(size)

    def putpixel(self, a: tuple[int, int],
                 color: tuple[int, int, int] = (0, 0, 0)) -> None:

        self.surface.set_at(a, color)

    def draw_line(self, a: tuple[int, int], b: tuple[int, int],
                  width: int = 1,
                  color: tuple[int, int, int] = (0, 0, 0),
                  ) -> None:

        pygame.draw.line(self.surface, color, a, b, width)

    def draw_rect(self, a: tuple[int, int], b: tuple[int, int],
                  color: tuple[int, int, int] = (0, 0, 0)) -> None:

        pygame.draw.rect(self.surface, color, (*a, b[0] - a[0], b[1] - a[1]))

        # (x1, y1), (x2, y2) = a, b
        # sx = 1 if x2 > x1 else -1
        # sy = 1 if y2 > y1 else -1

        # for y in range(y1, y2, sy):
        #     for x in range(x1, x2, sx):
        #         self.putpixel((x, y), color)

    def fill(self, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        self.draw_rect((0, 0), self.size, color=color)

    def put_image(self, a: tuple[int, int], image: pygame.Surface) -> None:
        self.surface.blit(image, a)

    def update_size(self, new_size: tuple[int, int]) -> None:
        self.size = new_size

        self.surface = pygame.Surface(new_size)


def print_life(
        frame: Drawer, a: tuple[int, int], gap: int,
        life: int, alive: pygame.Surface, dead: pygame.Surface):

    LIFE = 3

    for i in range(LIFE):
        x, y = a
        if i < life:
            frame.put_image((x + i * gap, y), alive)
        else:
            frame.put_image((x + i * gap, y), dead)


def print_title(frame: Drawer):
    w, h = frame.size
    title_font = pygame.font.Font("assets/font/title.otf", h // 2)

    rendered_title = title_font.render("PAC-MAN", True, theme.TITLE.value)

    w_text, h_text = rendered_title.get_size()
    frame.surface.blit(
        rendered_title,
        (w // 2 - w_text // 2, h // 2 - h_text // 2),
    )
