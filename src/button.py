import pygame

from .drawing.basic_drawer import Drawer


class Button:
    def __init__(self, frame: Drawer, a: tuple[int, int],
                 i: float, size: int, text: str) -> None:
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
        self.pos = (w // 2 + self.padding_x, int(self.i * self.padding_y))

        self.rendered_text = self.font.render(self.text, False, (100, 80, 0))

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
