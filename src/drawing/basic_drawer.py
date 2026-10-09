import pygame

from ..color_utils import Theme
from ..utils import Timer, Color, Pos, Size


Icon = tuple[pygame.Surface, pygame.Surface, pygame.Surface]


class Drawer:
    def __init__(self, size: Size) -> None:
        """
        Initialise the Frame

        Args:
            size (tuple[int, int]) dimensions of the frame
        """
        self.size = size

        self.surface = pygame.Surface(size)

    # def putpixel(self, a: Pos, color: Color = (0, 0, 0)) -> None:

    #     self.surface.set_at(a, color)

    def draw_line(self, a: Pos, b: Pos,
                  width: int = 1, color: Color = (0, 0, 0)) -> None:

        pygame.draw.line(self.surface, color, a, b, width)

    def putpixel(self, a: Pos, color: Color = (0, 0, 0)) -> None:
        self.surface.set_at(a, color)

    def draw_rect(self, a: Pos, b: Pos, color: Color = (0, 0, 0)) -> None:

        pygame.draw.rect(self.surface, color, (*a, b[0] - a[0], b[1] - a[1]))

        # (x1, y1), (x2, y2) = a, b
        # sx = 1 if x2 > x1 else -1
        # sy = 1 if y2 > y1 else -1

        # for y in range(y1, y2, sy):
        #     for x in range(x1, x2, sx):
        #         self.putpixel((x, y), color)

    def fill(self, color: Color = (0, 0, 0)) -> None:
        self.draw_rect((0, 0), self.size, color=color)

    def put_image(self, a: Pos, image: pygame.Surface) -> None:
        self.surface.blit(image, a)

    def update_size(self, new_size: Size) -> None:
        self.size = new_size

        self.surface = pygame.Surface(new_size)


def print_theme(frame: Drawer, theme: Theme, font: pygame.font.Font,
                prev_bottom: int) -> None:
    w, h = frame.size

    rendered = font.render(theme.name, True, theme.header.title)

    w_text, h_text = rendered.get_size()

    frame.surface.blit(
        rendered, (w // 2 - w_text // 2, h // 2 - h_text // 2 + prev_bottom)
    )


def print_life(
        frame: Drawer, a: Pos, gap: int,
        life: int, icons: Icon, color: Color) -> None:

    LIFE = 3

    alive, dead, reflect = icons

    for i in range(LIFE):
        x, y = a
        if i < life:
            tinted = alive.copy()
            tinted.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
            frame.put_image((x + i * gap, y), tinted)
            frame.put_image((x + i * gap, y), reflect)
        else:
            frame.put_image((x + i * gap, y), dead)


def print_title(frame: Drawer, font: pygame.font.Font, color: Color) -> int:
    w, h = frame.size

    rendered = font.render("PAC-MAN", True, color)

    w_text, h_text = rendered.get_size()
    return (
        frame.surface.blit(
            rendered, (w // 2 - w_text // 2, h // 2 - h_text // 2),
        ).bottom
    )


def print_score(frame: Drawer, font: pygame.font.Font, score: int,
                color: Color) -> tuple[int, int]:
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
        score_text_size: Size,
        timer: Timer, max_time: int,
        color: Color) -> None:

    w, h = frame.size
    padding_x, padding_y = w // 30, h // 20
    _, last_h_text = score_text_size

    time = max_time - timer.game_time

    rendered = font.render(
        f"Time: {time // 1000}.{(time % 1000) // 10}", True, color)
    w_text, _ = rendered.get_size()
    frame.surface.blit(
        rendered, (w - w_text - padding_x, padding_y + last_h_text)
    )
