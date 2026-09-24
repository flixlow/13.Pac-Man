from enum import Enum


# CLASSIC
class ClassicColor(Enum):
    NORTH = (55, 15, 180)
    WEST = (65, 25, 195)
    SOUTH = (255, 240, 0)
    EAST = (255, 255, 0)
    PACGUM = (255, 255, 255)
    FOURTY_TWO = (0, 0, 0)
    TITLE = (0, 0, 0)
    USERNAME = (255, 255, 255)
    SCORE = (255, 255, 0)
    MAZE_BG = (30, 30, 30)
    MENU_BG = (230, 200, 15)
    TITLE_BG = (255, 255, 255)
    HIGHSCORE_BG = (50, 75, 150)
    BACKGROUND = (255, 255, 255)


# NEON
class NeonColor(Enum):
    NORTH = (0, 255, 255)
    WEST = (255, 0, 200)
    SOUTH = (180, 0, 255)
    EAST = (0, 255, 120)
    PACGUM = (255, 255, 255)
    FOURTY_TWO = (255, 0, 100)
    TITLE = (255, 20, 147)
    USERNAME = (240, 240, 255)
    SCORE = (255, 255, 0)
    MAZE_BG = (10, 10, 25)
    MENU_BG = (20, 0, 40)
    TITLE_BG = (5, 5, 15)
    HIGHSCORE_BG = (40, 0, 80)
    BACKGROUND = (0, 0, 0)


# SUNSET
class SunsetColor(Enum):
    NORTH = (255, 94, 77)
    WEST = (255, 140, 66)
    SOUTH = (200, 50, 90)
    EAST = (255, 195, 0)
    PACGUM = (255, 245, 225)
    FOURTY_TWO = (60, 20, 40)
    TITLE = (90, 30, 50)
    USERNAME = (255, 255, 255)
    SCORE = (255, 220, 100)
    MAZE_BG = (45, 20, 50)
    MENU_BG = (255, 170, 120)
    TITLE_BG = (255, 225, 190)
    HIGHSCORE_BG = (120, 40, 90)
    BACKGROUND = (255, 240, 220)


# FOREST
class ForestColor(Enum):
    NORTH = (34, 110, 60)
    WEST = (60, 140, 80)
    SOUTH = (140, 100, 50)
    EAST = (180, 140, 70)
    PACGUM = (240, 255, 220)
    FOURTY_TWO = (20, 40, 25)
    TITLE = (30, 60, 35)
    USERNAME = (235, 245, 225)
    SCORE = (255, 215, 90)
    MAZE_BG = (18, 30, 22)
    MENU_BG = (170, 200, 140)
    TITLE_BG = (225, 240, 200)
    HIGHSCORE_BG = (40, 80, 60)
    BACKGROUND = (245, 250, 235)


# Mono
class MonoColor(Enum):
    NORTH = (90, 90, 90)
    WEST = (110, 110, 110)
    SOUTH = (150, 150, 150)
    EAST = (170, 170, 170)
    PACGUM = (255, 255, 255)
    FOURTY_TWO = (20, 20, 20)
    TITLE = (0, 0, 0)
    USERNAME = (220, 220, 220)
    SCORE = (190, 190, 190)
    MAZE_BG = (15, 15, 15)
    MENU_BG = (40, 40, 40)
    TITLE_BG = (230, 230, 230)
    HIGHSCORE_BG = (60, 60, 60)
    BACKGROUND = (245, 245, 245)


# HORROR
class HorrorColor(Enum):
    NORTH = (120, 0, 0)
    WEST = (90, 10, 20)
    SOUTH = (60, 90, 50)
    EAST = (100, 120, 60)
    PACGUM = (230, 220, 200)
    FOURTY_TWO = (10, 0, 0)
    TITLE = (160, 0, 0)
    USERNAME = (200, 190, 175)
    SCORE = (220, 30, 30)
    MAZE_BG = (12, 8, 8)
    MENU_BG = (25, 10, 10)
    TITLE_BG = (5, 0, 0)
    HIGHSCORE_BG = (50, 0, 0)
    BACKGROUND = (0, 0, 0)


# KAWAII
class KawaiiColor(Enum):
    NORTH = (255, 182, 213)
    WEST = (255, 200, 221)
    SOUTH = (189, 224, 254)
    EAST = (162, 210, 255)
    PACGUM = (255, 255, 240)
    FOURTY_TWO = (120, 80, 140)
    TITLE = (255, 105, 180)
    USERNAME = (255, 250, 250)
    SCORE = (255, 223, 128)
    MAZE_BG = (150, 130, 200)
    MENU_BG = (255, 230, 240)
    TITLE_BG = (224, 247, 250)
    HIGHSCORE_BG = (205, 180, 219)
    BACKGROUND = (255, 245, 250)


# TASTYCROUSTY
class TastyCroustyColor(Enum):
    NORTH = (0, 240, 255)
    WEST = (0, 190, 235)
    SOUTH = (255, 40, 150)
    EAST = (255, 105, 180)
    PACGUM = (255, 240, 170)
    FOURTY_TWO = (255, 150, 30)
    TITLE = (255, 255, 255)
    USERNAME = (190, 255, 255)
    SCORE = (255, 225, 60)
    MAZE_BG = (22, 8, 42)
    MENU_BG = (255, 105, 180)
    TITLE_BG = (22, 8, 42)
    HIGHSCORE_BG = (0, 240, 255)
    BACKGROUND = (8, 3, 25)


class BackroomsColor(Enum):
    NORTH = (232, 210, 70)
    WEST = (212, 190, 55)
    SOUTH = (180, 158, 35)
    EAST = (245, 225, 95)
    PACGUM = (255, 252, 225)
    FOURTY_TWO = (195, 203, 110)
    TITLE = (70, 58, 8)
    USERNAME = (255, 250, 200)
    SCORE = (255, 240, 60)
    MAZE_BG = (156, 147, 88)
    MENU_BG = (222, 198, 60)
    TITLE_BG = (250, 235, 130)
    HIGHSCORE_BG = (140, 120, 25)
    BACKGROUND = (58, 49, 10)


THEMES: dict[str, type[Enum]] = {
    "classic": ClassicColor,
    "neon": NeonColor,
    "sunset": SunsetColor,
    "forest": ForestColor,
    "mono": MonoColor,
    "horror": HorrorColor,
    "kawaii": KawaiiColor,
    "crousty": TastyCroustyColor,
    "backroom": BackroomsColor
}


class Theme:
    def __init__(self, default: str) -> None:
        self.name = default
        self._names = list(THEMES)
        self._palette = THEMES[default]

    def set(self, name: str) -> None:
        self.name = name
        self._palette = THEMES[name]

    def cycle(self) -> str:
        i = self._names.index(self.name)
        self.set(self._names[(i + 1) % len(self._names)])
        return self.name

    def __getattr__(self, attr: str) -> Enum:
        return self._palette[attr]


theme = Theme("backroom")
