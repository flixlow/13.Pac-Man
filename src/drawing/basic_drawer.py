import pygame

from ..color_utils import Theme
from ..utils import Timer


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
        life: int, alive: pygame.Surface, dead: pygame.Surface
    ):

    LIFE = 3

    for i in range(LIFE):
        x, y = a
        if i < life:
            frame.put_image((x + i * gap, y), alive)
        else:
            frame.put_image((x + i * gap, y), dead)

Color = tuple[int, int, int]

def print_title(frame: Drawer, font: pygame.font.Font, color: Color) -> None:
    w, h = frame.size

    rendered = font.render("PAC-MAN", True, color)

    w_text, h_text = rendered.get_size()
    frame.surface.blit(
        rendered, (w // 2 - w_text // 2, h // 2 - h_text // 2),
    )

def print_score(frame: Drawer, font: pygame.font.Font, score: int, color: Color) -> int:
    w, h = frame.size
    padding_x, padding_y = w // 30, h // 20

    rendered = font.render(f"Score: {score}", True, color)
    w_text, h_text = rendered.get_size()
    frame.surface.blit(
        rendered, (w - w_text - padding_x, padding_y)
    )

    return w_text, h_text

def print_timer(
        frame: Drawer, font: pygame.font.Font,
        score_text_size: tuple[int, int],
        timer: Timer, max_time: int,
        color: Color
    ) -> None:

    w, h = frame.size
    padding_x, padding_y = w // 30, h // 20
    _, last_h_text = score_text_size

    time = max_time - timer.game_time

    rendered = font.render(f"Time: {time // 1000}.{(time % 1000) // 10}", True, color)
    w_text, _ = rendered.get_size()
    frame.surface.blit(
        rendered, (w - w_text - padding_x, padding_y + last_h_text)
    )

