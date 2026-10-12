"""Theme configuration and selection system.

This module validates JSON theme files and exposes the active palette to the
rest of the game.
"""

from pathlib import Path
import json
from typing import Annotated
from pydantic import (
    AfterValidator, BaseModel, ConfigDict, StrictInt, ValidationError,
    Field
)


def validate_color(color: tuple[int, int, int]) -> tuple[int, int, int]:
    """Validate that an RGB tuple is within the 0-255 range.

    Args:
        color: RGB tuple to validate.

    Returns:
        The validated color tuple.

    Raises:
        ValueError: If one component is outside the valid range.
    """
    if any(not 0 <= component <= 255 for component in color):
        raise ValueError("RGB color components must be between 0 and 255")
    return color


Color = Annotated[
    tuple[StrictInt, StrictInt, StrictInt], AfterValidator(validate_color)
]


class StrictModel(BaseModel):
    """Base model that forbids unknown fields."""
    model_config = ConfigDict(extra="forbid")


class Walls(StrictModel):
    """Wall colors for each side of a maze cell."""
    north: Color
    west: Color
    south: Color
    east: Color


class Maze(StrictModel):
    """Color palette used by a maze theme."""
    walls: Walls
    background: Color
    forty_two_logo: Color


class Header(StrictModel):
    """Header UI colors."""
    title: Color
    score: Color
    timer: Color
    background: Color
    heart_color: Color


class Leaderboard(StrictModel):
    """Leaderboard color palette."""
    background: Color
    username: Color
    score: Color


class Buttons(StrictModel):
    """Button colors."""
    background: Color
    text: Color


class Menu(StrictModel):
    """Menu panel colors."""
    leaderboard: Leaderboard
    buttons: Buttons


class Interface(StrictModel):
    """Global UI colors."""
    header: Header
    menu: Menu
    background: Color


class Config(StrictModel):
    """Theme-specific animation toggles."""
    crazy_animation: bool
    pacgum_animation: bool


class JSONTheme(StrictModel):
    """Theme file schema loaded from JSON.

    Attributes:
        name: Display name of the theme.
        maze: Palette for the normal maze.
        crazy_maze: Palette for crazy mode.
        interface: UI colors.
        config: Animation flags.
        pacgum: Pac-gum dot color.
    """

    name: str = Field(min_length=1)
    maze: Maze
    crazy_maze: Maze
    interface: Interface
    config: Config
    pacgum: Color


def load_theme(filename: Path) -> JSONTheme:
    """Load and validate a theme file.

    Args:
        filename: Path to a JSON theme file.

    Returns:
        Parsed and validated theme model.
    """
    with open(filename, "r") as f:
        content = json.load(f)

    return JSONTheme.model_validate(content)


class Theme:
    """Resolved theme object used at runtime by the drawing stack."""

    def __init__(self, theme: JSONTheme) -> None:
        """Initialize the runtime theme wrapper.

        Args:
            theme: Source JSON theme model.
        """
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
    """Manage the list of themes and the currently selected one."""

    def __init__(self) -> None:
        """Initialize the theme list and selected index."""
        self.themes: list[Theme] = []
        self.selected_index = 0
        self.load_all_themes()

    @property
    def current_theme(self) -> Theme:
        """Return the currently selected theme."""
        return self.get_selected()

    def load_all_themes(self) -> bool:
        """Load all default and user-defined theme files.

        Returns:
            True if at least one valid theme was loaded.
        """
        from .utils import Paths

        default_directory = Path(Paths.DEFAULT_THEMES)
        user_directory = Path(Paths.THEMES)

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
        """Return the selected theme.

        Returns:
            Active theme instance.
        """
        return self.themes[self.selected_index]

    def cycle(self) -> Theme:
        """Select the next theme in the list.

        Returns:
            Newly selected theme instance.
        """
        self.selected_index += 1
        self.selected_index %= (len(self.themes))
        return self.get_selected()
