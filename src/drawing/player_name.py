"""Player name prompt rendering for leaderboard input."""

from typing import Any
import pygame

from .basic_drawer import Drawer
from ..utils import Timer, Paths


class PlayerName:
    """Handle rendering and editing of the player-name input field.

    Args:
        size: Dimensions of the input frame.
        timer: Global timer used for blinking cursor animation.
    """

    def __init__(self, size: tuple[int, int], timer: Timer) -> None:
        """Initialize the input field.

        Args:
            size: Dimensions of the screen area for the name prompt.
            timer: Shared timer used for blinking effects.
        """
        w, _ = size

        self.frame = Drawer(size)
        self.timer = timer

        self.background_color = (0, 0, 0)
        self.title_color = (255, 255, 255)
        self.name_color = (0, 0, 0)
        self.cursor_color = (0, 0, 0)

        self.cursor: int = 0
        self.name: list[str] = []

        self.render()

    def clear(self) -> None:
        """Clear the current name and reset the text cursor."""
        self.cursor = 0
        self.name = []

    def _get_font_size(self, text: str, font_path: str,
                       max_width: int, max_height: int,
                       ref_size: int = 100) -> int:
        """Compute a font size that fits in the available box.

        Args:
            text: Text to measure.
            font_path: Path to the font file.
            max_width: Maximum allowed width.
            max_height: Maximum allowed height.
            ref_size: Initial reference size for scaling.

        Returns:
            Suitable font size for the text.
        """
        if not text:
            return ref_size

        ref_font = pygame.font.Font(font_path, ref_size)
        tw, th = ref_font.size(text)

        scale = min(max_width / tw, max_height / th)
        return max(1, int(ref_size * scale))

    def render(self) -> None:
        """Refresh the frame content and redraw the name prompt."""
        w, h = self.frame.size

        self.padding_x, self.padding_y = w // 10, h // 10

        # font
        self.title_font = pygame.font.Font("assets/font/title.otf", w // 20)

        box_w = w - 2 * self.padding_x - 20
        box_h = (h // 2 - 2 * self.padding_y) - 20

        name_text = "".join(self.name)
        name_size = self._get_font_size(
            name_text, Paths.LEADERBOARD, box_w, box_h
        )
        self.name_font = pygame.font.Font(Paths.LEADERBOARD, name_size)

        # rendered
        self.rendered_title = self.title_font.render(
            "Enter Your Name:", False, self.title_color)
        self.rendered_name = self.name_font.render(
            name_text, False, self.name_color
        )

        wt, ht = self.rendered_name.get_size()

        self.frame.fill(self.background_color)
        self.frame.draw_rect(
            (self.padding_x, h // 2 + self.padding_y),
            (w - self.padding_x, h // 2 - self.padding_y + h // 2),
            (255, 255, 255)
        )

        self.frame.surface.blit(
            self.rendered_title,
            (
                (w - self.rendered_title.get_width()) // 2,
                h // 2 - self.padding_y - self.rendered_title.get_height() - 10
            )
        )

        self.frame.surface.blit(
            self.rendered_name,
            (
                (w // 2 - wt // 2),
                (h // 2 + self.padding_y) +
                (h // 2 - 2 * self.padding_y) // 2 - ht // 2
            )
        )

        is_displayed = (self.timer.total_spend_time // 500) % 2 == 0

        if self.name and is_displayed:
            self.display_cursor()

    def handle_player_name_input(self, event: Any) -> None:
        """Process keyboard input to modify the current player name.

        Args:
            event: pygame key event.
        """
        if event.key == pygame.K_UP:
            self.cursor = 0
        elif event.key == pygame.K_DOWN:
            self.cursor = len(self.name)
        elif event.key == pygame.K_RIGHT:
            self.cursor = min(self.cursor + 1, len(self.name))
        elif event.key == pygame.K_LEFT:
            self.cursor = max(self.cursor - 1, 0)
        elif event.key == pygame.K_BACKSPACE:
            if self.name and self.cursor:
                self.name.pop(self.cursor - 1)
            self.cursor = max(0, self.cursor - 1)
        else:
            if len(self.name) < 10:
                self.name.insert(self.cursor, event.unicode)
                self.cursor += 1

        self.render()

    def display_cursor(self) -> None:
        """Render the text cursor at the current insertion position."""
        w, h = self.frame.size
        wt, ht = self.rendered_name.get_size()

        txt = "".join(self.name[i] for i in range(self.cursor))
        fw, fh = self.name_font.size(txt)

        x1 = w // 2 - wt // 2 + fw
        y1 = (
            (h // 2 + self.padding_y) +
            (h // 2 - 2 * self.padding_y) // 2 - ht // 2
        )

        x2 = x1
        y2 = y1 + ht

        self.frame.draw_line(
            (x1, y1), (x2, y2), width=3, color=self.cursor_color
        )

    def get_frame(self) -> Drawer:
        """Return the underlying drawer used to display the prompt.

        Returns:
            The surface wrapper containing the drawn prompt.
        """
        return self.frame
