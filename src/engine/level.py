
from random import shuffle, random

from .maze import Maze
from ..utils import Direction, Timer, TypeScore, OPPOSITE
from ..entity import Entity, Ghost, Player, Blue, Red, Pink, Orange, Secret


class Level:
    def __init__(self, maze: Maze, t: Timer) -> None:
        self.maze: Maze = maze
        self.timer: Timer = t

        self.eaten: dict[TypeScore, int] = {}
        self.on_godmode: bool = False
        self.is_completed: bool = False
        self.on_crazy_mode: bool = False

        self._init_entities()
        self._init_pacgums()

    @staticmethod
    def _render_position(entity: Entity) -> tuple[float, float]:
        progress = min(
            entity.animation_elapsed_ms / max(1, entity.movement_interval_ms),
            1.0,
        )
        start_x, start_y = entity.previous_coords
        end_x, end_y = entity.coords
        return (
            start_x + (end_x - start_x) * progress,
            start_y + (end_y - start_y) * progress,
        )

    def _init_pacgums(self) -> None:
        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()

        for x in range(self.maze.w):
            for y in range(self.maze.h):
                if self.maze.maze_map[y][x] == 15:
                    continue
                if (x, y) in self.maze.corners:
                    self.super_pacgums.add((x, y))
                self.pacgums.add((x, y))

    def _init_ghosts(self) -> None:
        ghost_classes: list[type[Ghost]] = [Blue, Red, Orange, Pink]

        shuffle(ghost_classes)

        if random() < 0.5:
            ghost_classes[0] = Secret

        for ghost_class, coords in zip(ghost_classes, self.maze.corners):
            new_ghost = ghost_class(coords, self.maze, self.timer, self.player)
            self.ghosts.append(new_ghost)
            self.entities.append(new_ghost)

    def _init_player(self) -> None:
        start_pos = ((self.maze.w // 2 - 1), (self.maze.h // 2 - 1))
        self.player = Player(start_pos, self.maze, self.timer)

        self.entities.append(self.player)

    def _init_entities(self) -> None:
        self.ghosts: list[Ghost] = []
        self.entities: list[Entity] = []

        self._init_player()
        self._init_ghosts()

    def set_crazy_mode(self, status: bool) -> None:
        self.on_crazy_mode = status

        for e in self.entities:
            e.crazy_mode = status

    def count_eaten(self, score_type: TypeScore) -> None:
        self.eaten[score_type] = (self.eaten.get(score_type, 0) + 1)

    def change_direction(self, new_direction: Direction) -> None:
        if self.player.direction != Direction.START\
                and OPPOSITE.get(self.player.direction) == new_direction:
            self.player.reverse(new_direction)
        elif self.player.direction == new_direction:
            return
        else:
            self.player.next_direction = new_direction

    def check_crazy_mode(self) -> None:
        if self.on_crazy_mode is True:
            self.timer.crazy_mode_elapsed_time += self.timer.elapsed_time
            if self.timer.crazy_mode_elapsed_time >= 5000:
                self.timer.crazy_mode_elapsed_time = 0
                self.set_crazy_mode(False)

    def check_collision(self) -> None:
        for g in self.ghosts:
            if not g.is_alive:
                continue
            if g.coords == self.player.coords:
                if self.on_godmode or self.on_crazy_mode:
                    self.count_eaten(TypeScore.GHOST)
                    g.respawn()
                else:
                    self.player.is_alive = False

    def is_pacgum_here(self) -> None:
        if self.player.coords in self.pacgums:
            if self.player.coords in self.maze.corners:
                self.count_eaten(TypeScore.SUPER_PACGUM)
                self.set_crazy_mode(True)
                self.timer.crazy_mode_elapsed_time = 0
                self.super_pacgums.remove(self.player.coords)
            else:
                self.count_eaten(TypeScore.PACGUM)

            self.pacgums.remove(self.player.coords)

        if not self.pacgums:
            self.is_completed = True

    def update(self) -> None:
        self.check_crazy_mode()

        if self.player.noclip:
            self.player.move_with_noclip()
        else:
            self.player.move()

        self.check_collision()

        for g in self.ghosts:
            g.move()

        self.check_collision()

        self.is_pacgum_here()
