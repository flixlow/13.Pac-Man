import pygame


class Frame:
    def __init__(self, size: tuple[int, int]) -> None:
        """
        Initialise the Frame

        Args:
            size (tuple[int, int]) dimensions of the frame
        """
        self.surface = pygame.Surface(size)
        self.size = size

    def putpixel(self, a: tuple[int, int],
                 color: tuple[int, int, int] = (0, 0, 0)) -> None:

        self.surface.set_at(a, color)

    def draw_circle(self, a: tuple[int, int], radius: int, filled: bool = True,
                    color: tuple[int, int, int] = (255, 255, 255),
                    ) -> None:
        x = 0
        y = radius
        d = 3 - 2 * radius
        cx, cy = a
        if not filled:
            while x <= y:
                self.putpixel((cx + x, cy + y), color)
                self.putpixel((cx - x, cy + y), color)
                self.putpixel((cx + x, cy - y), color)
                self.putpixel((cx - x, cy - y), color)
                self.putpixel((cx + y, cy + x), color)
                self.putpixel((cx - y, cy + x), color)
                self.putpixel((cx + y, cy - x), color)
                self.putpixel((cx - y, cy - x), color)

                if d < 0:
                    d = d + 4 * x + 6
                else:
                    d = d + 4 * (x - y) + 10
                    y -= 1

                x += 1
        else:
            for y in range(-radius, radius + 1):
                for x in range(-radius, radius + 1):
                    if x * x + y * y <= radius * radius:
                        self.putpixel((cx + x, cy + y), color)

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
