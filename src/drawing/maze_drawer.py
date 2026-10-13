"""Maze rendering logic for the game board.

This module contains the `MazeDrawer`, which computes tile sizes, wall offsets
and draws the maze cells using the active theme.
"""

from .basic_drawer import Drawer
from ..engine.maze import Maze
from ..theme_selection import ThemeSelection, Theme

Color = tuple[int, int, int]


class MazeDrawer(Drawer):
    """Render the maze using the selected theme and a set of wall flags.

    Args:
        size: Dimensions of the drawing surface.
        maze: Maze configuration to render.
        theme_selection: Theme manager used to resolve active colors.
    """

    def __init__(self, size: tuple[int, int],
                 maze: Maze, theme_selection: ThemeSelection) -> None:
        """Initialize the maze drawer with a surface size and maze data.

        Args:
            size: Width and height of the drawing surface in pixels.
            maze: Maze object containing the map and layout metadata.
            theme_selection: Theme manager that provides the active colors.
        """
        super().__init__(size)

        self.maze = maze.maze_map
        self.maze_height = maze.h
        self.maze_width = maze.w
        self.theme_selection = theme_selection

        MazeDrawer.update_size(self, size)

        MazeDrawer.draw_maze(self)

    @staticmethod
    def _as_rgb(color: tuple[int, ...]) -> tuple[int, int, int]:
        """Convert a color tuple to a valid RGB triplet.

        Args:
            color: A color-like tuple.

        Returns:
            A normalized ``(r, g, b)`` tuple.

        Raises:
            ValueError: If the tuple does not contain exactly three channels.
        """
        if len(color) != 3:
            raise ValueError(f"Expected RGB color, got {color!r}")
        return color[0], color[1], color[2]

    @property
    def theme(self) -> Theme:
        """Return the currently active theme."""
        return self.theme_selection.current_theme

    def update_maze(self, maze: Maze) -> None:
        """Refresh the underlying maze data and recompute layout metrics.

        Args:
            maze: New maze instance.
        """
        self.maze = maze.maze_map
        self.maze_height = maze.h
        self.maze_width = maze.w
        self.update_size(self.size)

    def update_size(self, new_size: tuple[int, int]) -> None:
        """Update the drawing area and recompute cell-related metrics.

        Args:
            new_size: New surface dimensions in pixels.
        """
        super().update_size(new_size)

        self.cell_size = min(
            self.size[0] // self.maze_width,
            self.size[1] // self.maze_height
        )
        self.wall_width = 3 * max(1, (self.cell_size // 30))

        maze_width_px = self.maze_width * self.cell_size
        maze_height_px = self.maze_height * self.cell_size

        self.offset_x = (self.size[0] - maze_width_px) // 2
        self.offset_y = (self.size[1] - maze_height_px) // 2

    def draw_maze(self) -> None:
        """Render the full maze grid, including start and end cells."""

        self.fill(self.theme.maze.background)

        for y in range(self.maze_height):
            for x in range(self.maze_width):
                self.draw_cell(
                    self.maze[y][x], (x, y)
                )

    @staticmethod
    def _lerp(c1: Color, c2: Color, t: float) -> Color:
        """Linear interpolation between two RGB colors."""
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )

    def draw_cell(self, value: int, cell: tuple[int, int],
                  bg: Color | None = None, progress: float | None = None
                  ) -> None:
        """Render a single maze cell and its walls.

        Args:
            value: Bitmask describing the walls around the cell.
            cell: Tile coordinates in the maze grid.
            bg: Optional background color override for the cell.
            progress: Optional crazy-mode blend, 0 = normal, 1 = crazy.
        """
        x, y = cell

        px = x * self.cell_size + self.offset_x
        py = y * self.cell_size + self.offset_y

        x1, y1 = px, py
        x2, y2 = px + self.cell_size, py + self.cell_size

        t = progress if progress is not None else 0.0
        normal = self.theme.maze
        crazy = self.theme.crazy_maze
        lerp = MazeDrawer._lerp

        top = lerp(normal.walls.north, crazy.walls.north, t)
        left = lerp(normal.walls.west, crazy.walls.west, t)
        bottom = lerp(normal.walls.south, crazy.walls.south, t)
        right = lerp(normal.walls.east, crazy.walls.east, t)

        if bg is None:
            bg = lerp(normal.background, crazy.background, t)

        logo_color = lerp(normal.forty_two_logo, crazy.forty_two_logo, t)

        self.draw_rect((x1, y1), (x2, y2), bg)

        if value == 15:
            self.draw_rect((x1, y1), (x2, y2), logo_color)
            return

        if value & 1:
            self.draw_rect((x1, y1), (x2, y1 + self.wall_width), top)

        if value & 2:
            self.draw_rect((x2 - self.wall_width, y1), (x2, y2), left)

        if value & 4:
            self.draw_rect((x1, y2 - self.wall_width), (x2, y2), bottom)

        if value & 8:
            self.draw_rect((x1, y1), (x1 + self.wall_width, y2), right)
