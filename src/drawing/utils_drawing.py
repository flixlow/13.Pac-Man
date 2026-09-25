from typing import Any
import pygame

from .basic_drawer import Drawer
from ..utils import Timer


class PlayerScore:
    def __init__(self, size: tuple[int, int], timer: Timer) -> None:
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

    def _get_font_size(self, text: str, font_path: str,
                       max_width: int, max_height: int,
                       ref_size: int = 100) -> int:
        if not text:
            return ref_size

        ref_font = pygame.font.Font(font_path, ref_size)
        tw, th = ref_font.size(text)

        scale = min(max_width / tw, max_height / th)
        return max(1, int(ref_size * scale))

    def render(self) -> None:
        w, h = self.frame.size

        self.padding_x, self.padding_y = w // 10, h // 10

        # font
        self.title_font = pygame.font.Font("assets/font/title.otf", w // 20)

        box_w = w - 2 * self.padding_x - 20
        box_h = (h // 2 - 2 * self.padding_y) - 20

        name_text = "".join(self.name)
        name_size = self._get_font_size(
            name_text, "assets/font/leaderboard.ttf", box_w, box_h
        )
        self.name_font = pygame.font.Font(
            "assets/font/leaderboard.ttf", name_size
        )

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

    def jsp(self, event: Any) -> None:
        if event is None:
            print("bad key !")
            return False

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
            print("entire name: ", self.name)
        else:
            if len(self.name) < 20:
                self.name.insert(self.cursor, event.unicode)
                self.cursor += 1

        self.render()

    def display_cursor(self) -> None:
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
        return self.frame
