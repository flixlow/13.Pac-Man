import pygame


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


def print_life(frame: Drawer, a: tuple[int, int], life: int):
    TEST = 50

    frame.draw_rect(
        (a[0], a[1]), (a[0] + TEST * 3, a[1] + TEST)
    )

    for i in range(life):
        frame.draw_rect(
            (a[0] + i * TEST, a[1]),
            (a[0] + (i + 1) * TEST, a[1] + TEST),
            (255, 255//3*i, 0)
        )


def print_title(frame: Drawer):
    w, h = frame.size
    title_font = pygame.font.Font(None, h // 2)
    rendered_title = title_font.render(
        "PAC-MAN", True, (0, 0, 0)
    )
    w_text, h_text = rendered_title.get_size()
    frame.surface.blit(
        rendered_title,
        (w // 2 - w_text // 2, h // 2 - h_text // 2),
    )
