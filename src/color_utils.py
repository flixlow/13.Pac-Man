from pathlib import Path
import json
from typing import Annotated
from pydantic import (
    AfterValidator, BaseModel, ConfigDict, StrictInt, ValidationError,
    field_validator,
)


def validate_color(color: tuple[int, int, int]) -> tuple[int, int, int]:
    if any(not 0 <= component <= 255 for component in color):
        raise ValueError("RGB color components must be between 0 and 255")
    return color


Color = Annotated[
    tuple[StrictInt, StrictInt, StrictInt], AfterValidator(validate_color)
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Walls(StrictModel):
    north: Color
    west: Color
    south: Color
    east: Color


class Maze(StrictModel):
    walls: Walls
    background: Color
    forty_two_logo: Color


class Header(StrictModel):
    title: Color
    score: Color
    timer: Color
    background: Color
    heart_color: Color


class Leaderboard(StrictModel):
    background: Color
    username: Color
    score: Color


class Buttons(StrictModel):
    background: Color
    text: Color


class Menu(StrictModel):
    leaderboard: Leaderboard
    buttons: Buttons


class Interface(StrictModel):
    header: Header
    menu: Menu
    background: Color


class Config(StrictModel):
    crazy_animation: bool
    pacgum_animation: bool


class JSONTheme(StrictModel):
    name: str
    maze: Maze
    crazy_maze: Maze
    interface: Interface
    config: Config
    pacgum: Color

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("Theme name must not be empty")
        return name


def load_theme(filename: Path) -> JSONTheme:
    with open(filename, "r") as f:
        content = json.load(f)

    return JSONTheme.model_validate(content)


class Theme:
    def __init__(self, theme: JSONTheme) -> None:
        self.theme: JSONTheme = theme

        self.name = self.theme.name
        self.background = self.theme.interface.background

        self.maze = self.theme.maze
        self.crazy_maze = self.theme.crazy_maze

        self.pacgum_color = self.theme.pacgum

        self.header = self.theme.interface.header

        menu = self.theme.interface.menu
        self.leaderboard = menu.leaderboard
        self.buttons = menu.buttons

        self.crazy_animation = self.theme.config.crazy_animation
        self.pacgum_animation = self.theme.config.pacgum_animation


class ThemeSelection:
    def __init__(self) -> None:
        self.themes: list[Theme] = []
        self.selected_index = 0

    @property
    def current_theme(self) -> Theme:
        return self.get_selected()

    def load_all_themes(self) -> bool:
        default_directory = Path("assets/default_theme/")
        user_directory = Path("themes/")

        # default
        for theme in default_directory.glob("*.json"):
            try:
                raw = load_theme(theme)
            except (OSError, json.JSONDecodeError, ValidationError):
                print(f"warning! {theme} is not valid")
            else:
                clean = Theme(raw)
                self.themes.append(clean)

        # user
        for theme in user_directory.glob("*.json"):
            try:
                raw = load_theme(theme)
            except (OSError, json.JSONDecodeError, ValidationError):
                print(f"warning! {theme} is not valid")
            else:
                clean = Theme(raw)
                self.themes.append(clean)

        if not self.themes:
            return False
        return True

    def get_selected(self) -> Theme:
        return self.themes[self.selected_index]

    def cycle(self) -> Theme:
        self.selected_index += 1
        self.selected_index %= (len(self.themes))
        return self.get_selected()
