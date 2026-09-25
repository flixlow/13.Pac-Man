from pygame import Surface

from .basic_drawer import Drawer


class PlayerFrame:
    def __init__(self, size: tuple[int, int]) -> None:
        self.frame = Drawer(size)
        self.background_color = (0, 0, 0) # dev

    def _render(self) -> None:
        self.frame.fill(self.background_color)

    def get_frame(self) -> Drawer:
        return self.frame