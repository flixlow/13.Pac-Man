"""Drawing helpers for pygame surfaces.

This module provides a lightweight `Drawer` abstraction for drawing primitive
shapes, text and images onto a dedicated pygame surface.
"""

import pygame

from ..timer import Timer
from ..theme_selection import Theme
from ..utils import Color, Pos, Size
from ..assetloader import AssetLoader


Icon = tuple[pygame.Surface, pygame.Surface, pygame.Surface]


class Drawer:
    """Wrap a pygame surface and expose simple drawing primitives.

    Args:
        size: Dimensions of the backing surface as ``(width, height)``.
    """

    def __init__(self, size: Size) -> None:
        """Initialize the drawing surface.

        Args:
            size: Dimensions of the drawing frame in pixels.
        """
        self.size = size
        self.surface = pygame.Surface(size)

    def draw_line(self, a: Pos, b: Pos,
                  width: int = 1, color: Color = (0, 0, 0)) -> None:
        """Draw a line between two points.

        Args:
            a: Start point of the line.
            b: End point of the line.
            width: Thickness of the line in pixels.
            color: RGB color of the line.
        """
        pygame.draw.line(self.surface, color, a, b, width)

    def putpixel(self, a: Pos, color: Color = (0, 0, 0)) -> None:
        """Draw a single pixel at the given position.

        Args:
            a: Pixel coordinates.
            color: RGB color of the pixel.
        """
        self.surface.set_at(a, color)

    def draw_rect(self, a: Pos, b: Pos, color: Color = (0, 0, 0)) -> None:
        """Draw a rectangle defined by two opposite corners.

        Args:
            a: First corner of the rectangle.
            b: Opposite corner of the rectangle.
            color: Fill color of the rectangle.
        """
        pygame.draw.rect(self.surface, color, (*a, b[0] - a[0], b[1] - a[1]))

    def fill(self, color: Color = (0, 0, 0)) -> None:
        """Fill the whole surface with a color.

        Args:
            color: RGB color used to fill the surface.
        """
        self.draw_rect((0, 0), self.size, color=color)

    def put_image(self, a: Pos, image: pygame.Surface) -> None:
        """Blit an image onto the surface at the given position.

        Args:
            a: Position where the image is drawn.
            image: Surface to draw.
        """
        self.surface.blit(image, a)

    def update_size(self, new_size: Size) -> None:
        """Resize the internal drawing surface.

        Args:
            new_size: New dimensions in pixels.
        """
        self.size = new_size
        self.surface = pygame.Surface(new_size)


def print_theme(frame: Drawer, theme: Theme, font: pygame.font.Font,
                prev_bottom: int) -> None:
    """Render the current theme name centered in the frame.

    Args:
        frame: Drawer where the text is rendered.
        theme: Active theme containing the theme name.
        font: Font used to render the name.
        prev_bottom: Vertical offset to position the text under the title.
    """
    w, h = frame.size

    rendered = font.render(theme.name, True, theme.header.title)

    w_text, h_text = rendered.get_size()

    frame.surface.blit(
        rendered, (w // 2 - w_text // 2, h // 2 - h_text // 2 + prev_bottom)
    )


def print_life(
        frame: Drawer, a: Pos, gap: int,
        life: int, icons: Icon, color: Color) -> int:
    """Draw the life counter using alive/dead/reflect heart sprites.

    Args:
        frame: Target surface.
        a: Top-left position of the first icon.
        gap: Horizontal spacing between icons.
        life: Number of remaining lives.
        icons: Tuple of ``(alive, dead, reflect)`` sprites.
        color: Tint applied to the alive heart.

    Returns:
        int: the bottom pos of the life icons.
    """

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

    return a[1] + alive.get_height()


def print_title(frame: Drawer, font: pygame.font.Font, color: Color) -> int:
    """Render the game title and return the bottom coordinate.

    Args:
        frame: Target surface.
        font: Font used for the title.
        color: Title color.

    Returns:
        Bottom coordinate of the rendered title rect.
    """
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
    """Render the score text on the top-right corner.

    Args:
        frame: Target surface.
        font: Font used to render the score.
        score: Current score to display.
        color: Text color.

    Returns:
        A tuple of ``(width, height)`` for the rendered score text.
    """
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
    """Render the level timer below the score.

    Args:
        frame: Target surface.
        font: Font used to render the timer.
        score_text_size: Size of the score text to offset the timer.
        timer: Timer instance containing elapsed level time.
        max_time: Maximum allowed time for the level in milliseconds.
        color: Text color.
    """
    w, h = frame.size
    padding_x, padding_y = w // 30, h // 20
    _, last_h_text = score_text_size

    time = max_time - timer.level_time

    rendered = font.render(
        f"Time: {time // 1000}.{(time % 1000) // 10}", True, color)
    w_text, _ = rendered.get_size()
    frame.surface.blit(
        rendered, (w - w_text - padding_x, padding_y + last_h_text)
    )


def print_cheat(
        frame: Drawer, offset_y: int,
        godmode: bool, noclip: bool, ultra_vision: bool
) -> None:
    """Display which cheats are active.

    Args:
        frame: Target Surface.
        offset_y: The bottom left of the lifes
        godmode: True if this cheat is active.
        noclip: True if this cheat is active.
        ultra_vision: True if this cheat is active.
    """
    w, _ = frame.size
    booleans = [godmode, noclip, ultra_vision]
    icons = AssetLoader.load_cheat()

    icon_size = w // 30
    x = 0

    for icon, active in zip(icons, booleans):
        if active:
            icon = pygame.transform.scale(icon, (icon_size, icon_size))
            frame.put_image((x, offset_y), icon)
            x += icon_size

    return None
