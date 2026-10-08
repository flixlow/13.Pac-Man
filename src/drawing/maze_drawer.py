from .basic_drawer import Drawer
from ..engine.maze import Maze
from ..color_utils import ThemeSelection


class MazeDrawer(Drawer):
    def __init__(self, size: tuple[int, int],
                 maze: Maze, theme_selection: ThemeSelection) -> None:
        super().__init__(size)

        self.maze = maze.maze_map
        self.maze_height = maze.h
        self.maze_width = maze.w
        self.theme_selection = theme_selection

        MazeDrawer.update_size(self, size)

        MazeDrawer.draw_maze(self)

    @property
    def theme(self):
        return self.theme_selection.current_theme

    def update_maze(self, maze: Maze) -> None:
        self.maze = maze.maze_map
        self.maze_height = maze.h
        self.maze_width = maze.w
        self.update_size(self.size)

    def update_size(self, new_size: tuple[int, int]) -> None:
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
        """
        Render the full maze grid, including start and end cells.
        """

        self.fill(self.theme.maze.background)

        for y in range(self.maze_height):
            for x in range(self.maze_width):
                self.draw_cell(
                    self.maze[y][x], (x, y)
                )

    def draw_cell(self, value: int,
                  cell: tuple[int, int],
                  bg: tuple[int, int, int] | None = None,
                  progress: float | None = None,
                  ) -> None:

        x, y = cell

        px = x * self.cell_size + self.offset_x
        py = y * self.cell_size + self.offset_y

        x1, y1 = px, py
        x2, y2 = px + self.cell_size, py + self.cell_size

        colors = (
            [self.theme.maze.walls.north, self.theme.crazy_maze.walls.north],
            [self.theme.maze.walls.west, self.theme.crazy_maze.walls.west],
            [self.theme.maze.walls.south, self.theme.crazy_maze.walls.south],
            [self.theme.maze.walls.east, self.theme.crazy_maze.walls.east]
        )

        top, left, bottom, right = (
            color[0] if progress is None
            else tuple(int(c * progress) for c in color[1])
            for color in colors
        )

        if progress is not None:
            progress = 1.0 - progress
            r, g, b = self.theme.crazy_maze.background
            bg = (
                int(r * progress),
                int(g * progress),
                int(b * progress),
            )

        if bg is not None:
            self.draw_rect(
                (x1, y1),
                (x2, y2),
                bg
            )
        else:
            self.draw_rect(
                (x1, y1),
                (x2, y2),
                self.theme.maze.background
            )

        if progress is None:
            logo_color = self.theme.maze.forty_two_logo
        else:
            logo_color = self.theme.crazy_maze.forty_two_logo

        if value == 15:
            self.draw_rect(
                (x1, y1),
                (x2, y2),
                logo_color
            )
            return

        if value & 1:
            self.draw_rect(
                (x1, y1),
                (x2, y1 + self.wall_width),
                top
            )

        if value & 2:
            self.draw_rect(
                (x2 - self.wall_width, y1),
                (x2, y2),
                left
            )

        if value & 4:
            self.draw_rect(
                (x1, y2 - self.wall_width),
                (x2, y2),
                bottom
            )

        if value & 8:
            self.draw_rect(
                (x1, y1),
                (x1 + self.wall_width, y2),
                right
            )
