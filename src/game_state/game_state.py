from src.entity import (Speedy, Shadow, Bashful, Pokey,
                        Pacman, Character, Direction, Ghost, GhostState)
from src.maze import Grid, CellContents
from src.parsing.models import GameConfig
from src.game_state.collision import collides
from enum import Enum, auto
import math
import random


PACMAN_SPEED = 4.0
GHOST_SPEED = 3.0
LST_DIRECTION = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]


class GameStatus(Enum):
    PLAYING = auto()
    PAUSED = auto()
    LOST = auto()
    WON = auto()


class GameState:
    def __init__(self, grid: Grid, config: GameConfig) -> None:
        self.grid = grid
        self.config: GameConfig = config
        self.rng = random.Random()
        self.lives: int = self.config.lives
        self.eaten_ghost: int = 0
        self.score: int = 0
        self.level: int = 1
        self.wanted_direction: Direction = Direction.NONE
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

    def _reset_position(self) -> None:
        y, x = self.grid.center_grid
        self.pacman.position = (float(y), float(x))
        self.pacman.direction = Direction.NONE
        self.wanted_direction = Direction.NONE

        for ghost, corner in zip(self.ghosts, self.grid.corners_grid):
            y, x = corner
            ghost.direction = Direction.NONE
            ghost.position = (float(y), float(x))
            ghost.state = GhostState.HUNTER

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

    def _check_ghost_collision(self) -> None:
        for ghost in self.ghosts:
            if ghost.state == GhostState.HUNTER:
                if collides(self.pacman.position, ghost.position):
                    if self.invincible:
                        continue
                    self.lives -= 1
                    if self.lives == 0:
                        self.status = GameStatus.LOST
                        return
                    self._reset_position()
                    return
            elif ghost.state == GhostState.HUNTED:
                if collides(self.pacman.position, ghost.position):
                    points_ghost = self.config.points_ghost
                    self.score += points_ghost * (2**self.eaten_ghost)
                    self.eaten_ghost += 1
                    ghost.state = GhostState.EATEN

    def select_direction(self, direction: Direction) -> None:
        self.wanted_direction = direction

    def update(self, dt: float) -> None:
        if self.status != GameStatus.PLAYING:
            return

        self._advance(self.pacman, self.wanted_direction, dt)

        if self._is_on_cell(self.pacman.position):
            y, x = self.pacman.position
            cell = self.grid.get_cell(int(y), int(x))
            eaten = cell.update_cell_content()
            if eaten == CellContents.PACGUM:
                self.score += self.config.points_pacgum
            elif eaten == CellContents.SUPER_PACGUM:
                self.score += self.config.points_super_pacgum
            if (eaten != CellContents.EMPTY
               and self.grid.remaining_pacgums() == 0):
                self.status = GameStatus.WON

        if not self.ghosts_frozen:
            for ghost in self.ghosts:
                self._advance(ghost, self.rng.choice(LST_DIRECTION), dt)
        self._check_ghost_collision()


# if __name__ == "__main__":
    # from src.maze.loader import generate_maze
    # from src.parsing.parse_config import ConfigParser

    # config = ConfigParser().load_config('config.json', GameConfig)
    # gs = GameState(generate_maze(
    #     config.height, config.width, config.seed, config.pacgum), config)
    # print(gs.lives - 1, gs.config.points_pacgum)

    # try:
    #     generate_maze(500, 500, 42, 42)
    # except ValueError as e:
    #     print(e)

    # from src.maze.loader import generate_maze
    # config = GameConfig()
    # gs = GameState(generate_maze(config.height, config.width,
    #                              config.seed, config.pacgum), config)
    # print('départ', gs.pacman.position, gs.score)
    # gs.select_direction(Direction.RIGHT)
    # for _ in range(120):
    #     gs.update(1 / 60)
    # print('après 2 s', gs.pacman.position, gs.score, gs.status)
    # print([g.position for g in gs.ghosts])
