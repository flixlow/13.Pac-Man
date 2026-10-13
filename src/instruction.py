from .drawing.basic_drawer import Drawer
import pygame

Size = tuple[int, int]
Color = tuple[int, int, int]


class Instructions:
    def __init__(self, size: Size, theme) -> None:
        self.frame: Drawer = Drawer(size)
        self.content = """
                Controls

                ⬆️ ⬇️ ⬅️ ➡️ (or W / A / S / D): steer Pac-Man
                Space: start the game
                Esc: pause

                Goal
                Eat all the dots without getting caught by the ghosts to
                advance to the next level.

                Rules

                Dots: 10 points. Power pellets:
                50 points and make ghosts vulnerable.
                Eat ghosts for 200 points.
                Touching a ghost costs you a life. You have 3 lives.

                Tip: Save power pellets for when ghosts are close.
                """

    def render(self) -> None:
        w, h = self.frame.size

        title_font = pygame.font.Font("assets/font/title.otf", w // 20)
        basic_font = pygame.font.Font("assets/font/leaderboard.ttf", w // 30)

        self.rendered_title = title_font.render(
            "Instructions", True, (255, 255, 255))

        self.rendered_instructions = []

        for line in self.content.splitlines():
            if line.strip():
                self.rendered_instructions.append(
                    basic_font.render(line, True, (255, 255, 255))
                )

    def display(self) -> None:
        w, h = self.frame.size

        current_height = 0
        last_height = 50
        index = 0

        self.frame.fill((0, 0, 0))

        w_text, h_text = self.rendered_title.get_size()
        self.frame.surface.blit(
            self.rendered_title, (w // 2 - w_text // 2, current_height)
        )

        for line in self.content.splitlines():
            if line.strip():
                current_height += last_height
            else:
                w_text, h_text = self.rendered_instructions[index].get_size()
                self.frame.surface.blit(
                    self.rendered_instructions[index],
                    (w // 2 - w_text // 2, current_height)
                )
                last_height = h_text
                current_height += h_text
                index += 1
