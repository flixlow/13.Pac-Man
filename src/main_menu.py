from .drawing.basic_drawer import Drawer
from .scorer import Scorer

import pygame


class Menu:
    def __init__(self, size) -> None:
        self.frame = Drawer(size)
        self.frame.fill((0, 125, 175))

        # leaderboard
        self.scorer = Scorer("score.json")
        self.score = self.scorer._load()
        self.scorers_rendered = []

        # init render
        self.draw_menu()

    def draw_menu(self) -> None:
        self.frame.fill((0, 125, 175))
        self.render_leaderboard()
        self.print_leaderboard()

    def render_leaderboard(self) -> None:
        self.scorers_rendered = []

        w, h = self.frame.size
        self.frame.draw_rect((0, 0), (w // 2, h), (50, 75, 100))

        self.font_name = pygame.font.Font(None, h // 10)
        for i, (key, value) in enumerate(self.score.items()):
            if i >= 10:
                return None
            self.scorers_rendered.append(
                (value, self.font_name.render(
                    f"{i + 1}: {key} - " + f"{value}",
                    True, (255, 255, 255)))
            )

        self.scorers_rendered = sorted(self.scorers_rendered, reverse=True)

    def print_leaderboard(self) -> None:
        h = 0
        for i in range(len(self.scorers_rendered)):
            score, scorer = self.scorers_rendered[i]
            hv = scorer.get_height()
            self.frame.surface.blit(
                scorer,
                (0, h)
            )
            h += hv
