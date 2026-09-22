from .drawing.basic_drawer import Drawer
from .scorer import Scorer

import pygame
from pygame import Surface


class Menu:
    def __init__(self, size, scorer: Scorer) -> None:
        self.frame = Drawer(size)
        self.frame.fill((0, 125, 175))
        w, h = self.frame.size

        self.scorer: Scorer = scorer

        self.scorers_rendered: list[tuple[int, Surface, Surface]] = []

        self.play_button = Button(
            self.frame, (w // 2 + w // 10, 0 + h // 10), 0, 2, "PLAY")
        self.button_test = Button(
            self.frame, (w // 2 + w // 10, 0 + h // 10), 2.5, 1, "TEST1")
        self.button_test2 = Button(
            self.frame, (w // 2 + w // 10, 0 + h // 10), 4, 1, "TEST2")

        self.buttons = [self.play_button, self.button_test, self.button_test2]

        self.button = pygame.image.load(
            "assets/button/button.png")
        self.button_pressed = pygame.image.load(
            "assets/button/button_pressed.png")
        self.update_size()
        self.draw_menu()

    def draw_menu(self) -> None:
        self.frame.fill((230, 200, 15))
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
                f"{i + 1}: {key}   ", True, (255, 255, 255)
            )

            score = self.font_name.render(
                f"{value}", True, (255, 255, 0)
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
        self.frame.draw_rect((0, 0), (w // 2, h), (50, 75, 150))

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


class Button:

    def __init__(self, frame: Drawer, a: tuple[int, int],
                 i: int, size: int, text: str) -> None:
        self.pos = a
        self.frame = frame
        self.screen_origin = (0, 0)
        self.i = i + 1
        self.size = size
        self.text = text
        self.font = pygame.font.Font("assets/font/title.otf", 25)

        w, h = self.frame.size
        self.padding_x, self.padding_y = w // 20, h // 10

        self.button_original = pygame.image.load("assets/button/button.png")
        self.button_pressed_original = pygame.image.load(
            "assets/button/button_pressed.png"
        )
        self.button = self.button_original
        self.button_pressed = self.button_pressed_original

    def update_size(self) -> None:

        w, h = self.frame.size
        self.font = pygame.font.Font("assets/font/title.otf", w // 25)
        self.padding_x, self.padding_y = w // 20, h // 10
        self.pos = (w // 2 + self.padding_x, self.i * self.padding_y)

        self.rendered_text = self.font.render(self.text, None, (100, 80, 0))

        size = (
            max(1, w // 2 - self.padding_x * 2),
            max(1, self.padding_y * self.size),
        )

        self.button = pygame.transform.scale(self.button_original, size)
        self.button_pressed = pygame.transform.scale(
            self.button_pressed_original, size
        )

    def draw(self) -> None:
        if not self.is_clicked():
            self.frame.put_image(self.pos, self.button)
        else:
            self.frame.put_image(self.pos, self.button_pressed)

        mid = (
            self.pos[0] + self.button.get_width() // 2,
            self.pos[1] + self.button.get_height() // 2
        )
        text_x = mid[0] - self.rendered_text.get_width() // 2
        text_y = mid[1] - self.rendered_text.get_height() // 2

        self.frame.surface.blit(self.rendered_text, (text_x, text_y))

    def set_screen_origin(self, origin: tuple[int, int]) -> None:
        self.screen_origin = origin

    def is_clicked(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        origin_x, origin_y = self.screen_origin
        button_rect = pygame.Rect(
            self.pos[0],
            self.pos[1],
            self.button.get_width(),
            self.button.get_height(),
        )

        return (
            button_rect.collidepoint(mouse_x - origin_x, mouse_y - origin_y)
            and pygame.mouse.get_pressed()[0]
        )
