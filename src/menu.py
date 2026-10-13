"""Menu rendering and leaderboard UI."""

from .drawing.basic_drawer import Drawer
from .theme_selection import ThemeSelection, Theme
from .scorer import Scorer
from .button import Button
from .utils import Paths

import pygame
from typing import Any
from pygame import Surface


class Menu:
    """Render the main menu with leaderboard data and action buttons.

    Args:
        size: Dimensions of the menu surface.
        scorer: Leaderboard store.
        theme_selection: Theme manager.
    """

    def __init__(self, size: tuple[int, int], scorer: Scorer,
                 theme_selection: ThemeSelection) -> None:
        """Initialize the menu and create all buttons.

        Args:
            size: Dimensions of the menu surface.
            scorer: Score store to render in the leaderboard.
            theme_selection: Active theme selector.
        """
        self.frame = Drawer(size)

        w, h = self.frame.size

        self.scorer: Scorer = scorer
        self.theme_selection = theme_selection

        self.scorers_rendered: list[tuple[int, Surface, Surface]] = []

        pos = (w // 2 + w // 10, 0 + h // 10)
        self.play_button = Button(
            self.frame, pos, 0, 2.5, "Play", self.theme.buttons
        )
        self.clear_lb = Button(
            self.frame, pos, 3, 1.5, "Clear Leaderboard", self.theme.buttons
        )
        self.change_theme = Button(
            self.frame, pos, 5, 1.5, "Rules", self.theme.buttons
        )
        self.exit = Button(
            self.frame, pos, 7, 1.5, "Exit", self.theme.buttons
        )

        self.buttons = [
            self.play_button, self.clear_lb, self.change_theme, self.exit
        ]
        self.show_rules = False

        self.update_size()
        self.draw_menu()

    @property
    def theme(self) -> Theme:
        """Return the currently selected theme."""
        return self.theme_selection.current_theme

    def clear_leaderboard(self) -> None:
        """Clear the score table and redraw the menu."""
        try:
            self.scorer.clear()
        except Exception:
            print("[WARNING]: can't clear learderboard.")
        self.draw_menu()

    def draw_menu(self) -> None:
        """Re-render the menu background, leaderboard and buttons."""
        for button in self.buttons:
            button.set_new_color(self.theme.buttons)

        self.frame.fill(self.theme.buttons.background)
        if self.show_rules:
            self.print_rules()
        else:
            self.render_leaderboard()
            self.print_leaderboard()
        self.print_buttons()

    def print_rules(self) -> None:
        """Show the game rules in place of the leaderboard."""
        w, h = self.frame.size
        self.frame.draw_rect(
            (0, 0), (w // 2, h),
            self.theme.leaderboard.background)
        font = pygame.font.Font(Paths.LEADERBOARD, h // 15)
        lines = [
            "INSTRUCTIONS",
            "===CONTROLS===", "wasd / arrow Keys",
            "===RULES===", "eat all dots to advance.",
            "===SCORE===", "dots: 10 points", "power pellets: 50 points",
            "eat ghosts: 200 points", "touching a ghost costs one life."
        ]
        y = h // 10
        for line in lines:
            text = font.render(line, True, self.theme.leaderboard.username)
            self.frame.surface.blit(text, (w // 4 - text.get_width() // 2, y))
            y += text.get_height() + 12

    def update_size(self) -> None:
        """Resize the menu and update all button positions."""
        w, h = self.frame.size
        self.padding_x, self.padding_y = w // 20, h // 10

        for button in self.buttons:
            button.update_size()

    def print_buttons(self) -> None:
        """Draw all menu buttons on the frame."""
        for button in self.buttons:
            button.draw()

    def set_screen_origin(self, origin: tuple[int, int]) -> None:
        """Set the global origin used for click coordinates.

        Args:
            origin: (x, y) offset of the menu on the screen.
        """
        for button in self.buttons:
            button.set_screen_origin(origin)

    def render_leaderboard(self) -> None:
        """Prepare rendered leaderboard surfaces for display."""
        w, h = self.frame.size
        r = h / (w / 2)

        self.scorers_rendered = []
        self.font_name = pygame.font.Font(Paths.LEADERBOARD, w // 25)

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

    def check_buttons(self, event: Any) -> list[int]:
        """Return the indexes of buttons clicked by the user.

        Args:
            event: pygame event.

        Returns:
            List of activated button indexes.
        """
        return [
            idx for idx, button
            in enumerate(self.buttons) if button.is_clicked(event)
        ]

    def print_leaderboard(self) -> None:
        """Draw the leaderboard panel and text on the menu frame."""
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
