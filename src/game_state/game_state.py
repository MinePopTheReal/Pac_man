from src.entity import (Speedy, Shadow, Bashful, Pokey,
                        Pacman, Character, Direction, Ghost, GhostState)
from src.maze import Grid
from enum import Enum, auto
import math


PACMAN_SPEED = 4.0
GHOST_SPEED = 3.0


class GameStatus(Enum):
    PLAYING = auto()
    PAUSED = auto()
    LOST = auto()
    WON = auto()


class GameState:
    def __init__(self, grid: Grid, lives: int = 3) -> None:
        self.grid = grid
        self.lives = lives
        self.score: int = 0
        self.level: int = 1
        self.nb_pacgums: int
        self.status: GameStatus = GameStatus.PLAYING
        self.invincible: bool = False
        self.ghosts_frozen: bool = False
        self.pacman = self._spawn_pacman()
        self.ghosts = self._spawn_ghosts()

    def _spawn_pacman(self) -> Pacman:
        y, x = self.grid.center_grid
        pacman = Pacman(Direction.NONE, (float(y), float(x)), PACMAN_SPEED)
        return pacman

    def _spawn_ghosts(self) -> list[Ghost]:
        lst_ghosts: list[Ghost] = []
        classes = [Shadow, Pokey, Bashful, Speedy]

        for classe, corner in zip(classes, self.grid.corners_grid):
            y, x = corner
            ghost = classe(Direction.NONE, (float(y), float(x)),
                           GhostState.HUNTER, GHOST_SPEED)
            lst_ghosts.append(ghost)
        return lst_ghosts

    @staticmethod
    def _is_on_cell(coord: tuple[float, float]) -> bool:
        y, x = coord
        return y.is_integer() and x.is_integer()

    def _choose_direction(self, y: int, x: int,
                          wanted: Direction, current: Direction) -> Direction:
        if self.grid.can_move(y, x, wanted):
            return wanted
        if self.grid.can_move(y, x, current):
            return current
        return Direction.NONE

    def _next_cell(self, coord: tuple[float, float],
                   direction: Direction) -> tuple[float, float]:
        y, x = coord
        dy, dx = direction.value

        if self._is_on_cell(coord):
            return (float(y + dy), float(x + dx))

        ny = math.ceil(y) if dy > 0 else math.floor(y) if dy < 0 else y
        nx = math.ceil(x) if dx > 0 else math.floor(x) if dx < 0 else x

        return (float(ny), float(nx))

    def _advance(self, character: Character, wanted: Direction,
                 dt: float) -> None:
        if self._is_on_cell(character.position):
            py, px = character.position
            character.direction = self._choose_direction(
                int(py), int(px), wanted, character.direction)
            if character.direction == Direction.NONE:
                return

        ty, tx = self._next_cell(character.position, character.direction)
        y, x = character.position
        remains = abs(ty - y) + abs(tx - x)

        distance = character.speed * dt
        if distance >= remains:
            character.position = (ty, tx)
        else:
            character.movement(dt)

    def update(self, dt: float) -> None:
        if self.status != GameStatus.PLAYING:
            return
