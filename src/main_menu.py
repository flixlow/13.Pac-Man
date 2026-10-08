from .drawing.basic_drawer import Drawer
from .color_utils import ThemeSelection
from .scorer import Scorer
from .button import Button

import pygame
from pygame import Surface


class Menu:
    def __init__(self, size, scorer: Scorer,
                 theme_selection: ThemeSelection) -> None:
        self.frame = Drawer(size)
        # self.frame.fill((0, 0, 0))
        w, h = self.frame.size

        self.scorer: Scorer = scorer
        self.theme_selection = theme_selection

        self.scorers_rendered: list[tuple[int, Surface, Surface]] = []

        pos = (w // 2 + w // 10, 0 + h // 10)
        self.play_button = Button(self.frame, pos, 0, 2.5, "Play", self.theme.buttons)
        self.clear_lb = Button(self.frame, pos, 3, 1.5, "Clear Leaderboard", self.theme.buttons)
        self.change_theme = Button(self.frame, pos, 5, 1.5, "Change Theme", self.theme.buttons)
        self.exit = Button(self.frame, pos, 7, 1.5, "Exit", self.theme.buttons)

        self.buttons = [
            self.play_button, self.clear_lb, self.change_theme, self.exit
        ]

        self.update_size()
        self.draw_menu()

    @property
    def theme(self):
        return self.theme_selection.current_theme

    def clear_leaderboard(self) -> None:
        self.scorer.clear()
        self.scorer.scores = self.scorer.load()
        self.draw_menu()

    def draw_menu(self) -> None:
        for button in self.buttons:
            button.set_new_color(self.theme.buttons)

        self.frame.fill(self.theme.buttons.background)
        self.render_leaderboard()
        self.print_leaderboard()
        self.print_buttons()

    def update_size(self) -> None:
        w, h = self.frame.size
        self.padding_x, self.padding_y = w // 20, h // 10

        for button in self.buttons:
            button.update_size()

    def print_buttons(self) -> None:
        for button in self.buttons:
            button.draw()

    def set_screen_origin(self, origin: tuple[int, int]) -> None:
        for button in self.buttons:
            button.set_screen_origin(origin)

    def render_leaderboard(self) -> None:
        w, h = self.frame.size
        r = h / (w / 2)

        self.scorers_rendered = []
        self.font_name = pygame.font.Font(
            "assets/font/leaderboard.ttf", w // 25)

        self.max_width_user = 0
        self.max_width_score = 0

        for i, (key, value) in enumerate(
                list(self.scorer.scores.items())[:10]):
            if i >= r * 10:
                return None

            if len(key) > 15:
                key = key[:15] + "..."

            user = self.font_name.render(
                f"{i + 1}: {key}   ", True, self.theme.leaderboard.username
            )

            score = self.font_name.render(
                f"{value}", True, self.theme.leaderboard.score
            )

            self.max_width_user = max(self.max_width_user, user.get_width())
            self.max_width_score = max(self.max_width_score, score.get_width())

            self.scorers_rendered.append((value, user, score))

    def check_buttons(self, event: pygame.event) -> list[int]:
        return [
            idx for idx, button
            in enumerate(self.buttons) if button.is_clicked(event)
        ]

    def print_leaderboard(self) -> None:
        w, h = self.frame.size
        self.frame.draw_rect(
            (0, 0), (w // 2, h), self.theme.leaderboard.background
        )

        px, py = self.frame.size
        ox, oy = (
            px // 4 - self.max_width_user // 2 - self.max_width_score // 2,
            py // 10
        )

        for n, user, score in self.scorers_rendered:
            self.frame.surface.blit(
                user, (ox, oy)
            )
            self.frame.surface.blit(
                score, (ox + self.max_width_user, oy)
            )
            oy += max(
                user.get_height(), score.get_height()
            )
