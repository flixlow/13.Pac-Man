from .drawing.basic_drawer import Drawer
from .color_utils import theme
from .scorer import Scorer
from .button import Button

import pygame
from pygame import Surface


class Menu:
    def __init__(self, size, scorer: Scorer) -> None:
        self.frame = Drawer(size)
        self.frame.fill((0, 125, 175))
        w, h = self.frame.size

        self.scorer: Scorer = scorer

        self.scorers_rendered: list[tuple[int, Surface, Surface]] = []

        pos = (w // 2 + w // 10, 0 + h // 10)
        self.play_button = Button(self.frame, pos, 0, 2, "PLAY")
        self.settings = Button(self.frame, pos, 2, 2, "SETTINGS")
        self.clic = Button(self.frame, pos, 4, 2, "CLIC HERE")
        self.exit = Button(self.frame, pos, 6, 2, "EXIT")

        self.buttons = [self.play_button, self.settings, self.clic, self.exit]

        self.button = pygame.image.load(
            "assets/button/button.png")
        self.button_pressed = pygame.image.load(
            "assets/button/button_pressed.png")
        self.update_size()
        self.draw_menu()

    def draw_menu(self) -> None:
        self.frame.fill(theme.MENU_BG.value)
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
        w, _ = self.frame.size

        self.scorers_rendered = []
        self.font_name = pygame.font.Font(
            "assets/font/leaderboard.ttf", w // 25)

        self.max_width_user = 0
        self.max_width_score = 0

        for i, (key, value) in enumerate(self.scorer.scores.items()):
            if i >= 10:
                return None

            if len(key) > 15:
                key = key[:15] + "..."

            user = self.font_name.render(
                f"{i + 1}: {key}   ", True, theme.USERNAME.value
            )

            score = self.font_name.render(
                f"{value}", True, theme.SCORE.value
            )

            self.max_width_user = max(self.max_width_user, user.get_width())
            self.max_width_score = max(self.max_width_score, score.get_width())

            self.scorers_rendered.append((value, user, score))

    def check_buttons(self) -> list[int]:
        return [
            idx for idx, button
            in enumerate(self.buttons) if button.is_clicked()
        ]

    def print_leaderboard(self) -> None:
        w, h = self.frame.size
        self.frame.draw_rect((0, 0), (w // 2, h), theme.HIGHSCORE_BG.value)

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
