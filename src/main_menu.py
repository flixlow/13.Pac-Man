from .drawing.basic_drawer import Drawer
from .scorer import Scorer

import pygame
from pygame import Surface


class Menu:
    def __init__(self, size, scorer: Scorer) -> None:
        self.frame = Drawer(size)
        self.frame.fill((0, 125, 175))

        self.scorer: Scorer = scorer

        self.scorers_rendered: list[tuple[int, Surface, Surface]] = []

        self.draw_menu()

    def draw_menu(self) -> None:
        self.frame.fill((0, 125, 175))
        self.render_leaderboard()
        self.print_leaderboard()

    def render_leaderboard(self) -> None:
        w, _ = self.frame.size

        self.scorers_rendered = []
        self.font_name = pygame.font.Font(None, w // 25)

        self.max_width_user = 0
        self.max_width_score = 0

        for i, (key, value) in enumerate(self.scorer.scores.items()):
            if i >= 10:
                return None

            if len(key) > 15:
                key = key[:15] + "..."

            user = self.font_name.render(
                f"{i + 1}: {key}   ", True, (200, 200, 200)
            )

            score = self.font_name.render(
                f"{value}", True, (255, 255, 255)
            )

            self.max_width_user = max(self.max_width_user, user.get_width())
            self.max_width_score = max(self.max_width_score, score.get_width())

            self.scorers_rendered.append((value, user, score))

    def print_leaderboard(self) -> None:
        w, h = self.frame.size
        self.frame.draw_rect((0, 0), (w // 2, h), (50, 75, 100))

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
