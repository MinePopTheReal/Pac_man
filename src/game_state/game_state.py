from src.entity import (Speedy, Shadow, Bashful, Pokey,
                        Pacman, Direction, Ghost, GhostState)
from src.maze import Grid, CellContents, LST_DIRECTION
from src.parsing.models import GameConfig
from src.game_state.collision import collides
from src.maze.loader import generate_maze
from src.game_state.movement import (is_on_cell, advance, direction_home)
from enum import Enum, auto
import random


PACMAN_SPEED = 4.0
SPEED_MULTIPLIER = 2.0
SPEED_REDUCTION = 0.5
GHOST_SPEED = 3.0


class GameStatus(Enum):
    PLAYING = auto()
    PAUSED = auto()
    LOST = auto()
    WON = auto()


class GameState:
    def __init__(self, config: GameConfig) -> None:
        self.config: GameConfig = config
        self.rng = random.Random()
        self.level: int = 1
        self.grid: Grid = self._new_grid()
        self.lives: int = self.config.lives
        self.cheat_mode: bool = False
        self.invincible: bool = False
        self.ghosts_frozen: bool = False
        self.fast: bool = False
        self.slow: bool = False
        self.time_hunt_ghosts: float = 0.0
        self.eaten_ghosts: int = 0
        self.score: int = 0
        self.wanted_direction: Direction = Direction.NONE
        self.status: GameStatus = GameStatus.PLAYING
        self.pacman = self._spawn_pacman()
        self.ghosts = self._spawn_ghosts()
        self.corner_maps: list[list[list[int]]] = self._maps_for_corners()

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
            ghost.respawn_timer = 0.0
        self.time_hunt_ghosts = 0.0

    def _new_grid(self) -> Grid:
        seed = self.config.seed if self.level == 1 else 0
        return generate_maze(self.config.height, self.config.width, seed,
                             self.config.pacgum)

    def _build_level(self) -> None:
        self.grid = self._new_grid()
        self.corner_maps = self._maps_for_corners()
        self._reset_position()
        self.eaten_ghosts = 0

    def _next_level(self) -> None:
        if self.level < self.config.nb_level:
            self.level += 1
            self._build_level()
        else:
            self.status = GameStatus.WON

    def _maps_for_corners(self) -> list[list[list[int]]]:
        lst_maps: list[list[list[int]]] = []
        for corner in self.grid.corners_grid:
            y, x = corner
            lst_maps.append(self.grid.distances_from_cell(y, x))
        return lst_maps

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
                    self.score += points_ghost * (2**self.eaten_ghosts)
                    self.eaten_ghosts += 1
                    ghost.state = GhostState.EATEN
                    ghost.respawn_timer = self.config.timer_respawn_ghost

    def _start_ghosts_hunt(self) -> None:
        self.time_hunt_ghosts = self.config.timer_hunt_ghosts
        for ghost in self.ghosts:
            if ghost.state == GhostState.HUNTER:
                ghost.state = GhostState.HUNTED

    def _update_time_ghost_hunt(self, dt: float) -> None:
        if self.time_hunt_ghosts > 0:
            self.time_hunt_ghosts -= dt
            if self.time_hunt_ghosts <= 0:
                self.time_hunt_ghosts = 0.0
                for ghost in self.ghosts:
                    if ghost.state == GhostState.HUNTED:
                        ghost.state = GhostState.HUNTER

    def _update_respawn_ghost(self, dt: float) -> None:
        for ghost, corner in zip(self.ghosts, self.grid.corners_grid):
            if ghost.state == GhostState.EATEN and ghost.position == corner:
                ghost.respawn_timer -= dt
                if ghost.respawn_timer <= 0:
                    ghost.respawn_timer = 0.0
                    ghost.state = GhostState.HUNTER

    def switch_cheat_mode(self) -> None:
        self.cheat_mode = not self.cheat_mode

    def switch_invincible(self) -> None:
        if self.cheat_mode:
            self.invincible = not self.invincible

    def switch_ghosts_frozen(self) -> None:
        if self.cheat_mode:
            self.ghosts_frozen = not self.ghosts_frozen

    def skip_level(self) -> None:
        if self.cheat_mode:
            self._next_level()

    def add_extra_life(self) -> None:
        if self.cheat_mode:
            self.lives += 1

    def switch_speed_pacman(self) -> None:
        if self.cheat_mode:
            self.fast = not self.fast
            if self.fast:
                self.pacman.speed = PACMAN_SPEED * SPEED_MULTIPLIER
            else:
                self.pacman.speed = PACMAN_SPEED

    def switch_slow_ghosts(self) -> None:
        if self.cheat_mode:
            self.slow = not self.slow
            if self.slow:
                for ghost in self.ghosts:
                    ghost.speed = GHOST_SPEED * SPEED_REDUCTION
            else:
                for ghost in self.ghosts:
                    ghost.speed = GHOST_SPEED

    def select_direction(self, direction: Direction) -> None:
        self.wanted_direction = direction

    def update(self, dt: float) -> None:
        if self.status != GameStatus.PLAYING:
            return

        advance(self.pacman, self.wanted_direction, dt, self.grid)

        if is_on_cell(self.pacman.position):
            y, x = self.pacman.position
            cell = self.grid.get_cell(int(y), int(x))
            eaten = cell.update_cell_content()
            if eaten == CellContents.PACGUM:
                self.score += self.config.points_pacgum
            elif eaten == CellContents.SUPER_PACGUM:
                self.score += self.config.points_super_pacgum
                self.eaten_ghosts = 0
                self._start_ghosts_hunt()
            if (eaten != CellContents.EMPTY
               and self.grid.remaining_pacgums() == 0):
                self._next_level()
                return

        if not self.ghosts_frozen:
            for ghost, mapp in zip(self.ghosts, self.corner_maps):
                y, x = ghost.position
                if ghost.state == GhostState.EATEN:
                    if is_on_cell((y, x)):
                        wanted = direction_home(int(y), int(x), mapp,
                                                self.grid)
                    else:
                        wanted = ghost.direction
                else:
                    wanted = self.rng.choice(LST_DIRECTION)
                advance(ghost, wanted, dt, self.grid)
        self._update_time_ghost_hunt(dt)
        self._update_respawn_ghost(dt)
        self._check_ghost_collision()


if __name__ == "__main__":
    #     from src.maze.loader import generate_maze
    #     from src.parsing.parse_config import ConfigParser
    #     try:
    #         config = ConfigParser().load_config('config.json', GameConfig)
    #     except Exception as e:
    #         print(e)
    #     else:
    #         gs = GameState(generate_maze(
    #             config.height, config.width, config.seed, config.pacgum),
    #             config)
    #         print(gs.lives - 1, gs.config.points_pacgum)

    # try:
    #     generate_maze(500, 500, 42, 42)
    # except ValueError as e:
    #     print(e)

    # from src.maze.loader import generate_maze

    # config = GameConfig()
    # gs = GameState(generate_maze(config.height, config.width,
    #                              config.seed, config.pacgum), config)
    # for ghost in gs.ghosts:
    #     ghost.position = gs.pacman.position
    #     ghost.state = GhostState.HUNTED
    # gs._check_ghost_collision()
    # print(gs.score)

    # from src.maze.loader import generate_maze
    # from src.parsing.parse_config import ConfigParser

    # config = ConfigParser().load_config('config.json', GameConfig)
    # gs = GameState(generate_maze(config.height, config.width,
    #                              config.seed, config.pacgum), config)
    # gs.ghosts_frozen = True
    # y, x = gs.pacman.position
    # gs.grid.get_cell(int(y), int(x)).content = CellContents.SUPER_PACGUM
    # gs.update(0.01)
    # print('juste après :', gs.time_hunt_ghosts,
    #       [g.state.name for g in gs.ghosts])
    # for _ in range(500):
    #     gs.update(0.01)
    # print('après 5 s   :', round(gs.time_hunt_ghosts, 2),
    #       [g.state.name for g in gs.ghosts])
    # for _ in range(600):
    #     gs.update(0.01)
    # print('après 9 s   :', round(gs.time_hunt_ghosts),
    #       [g.state.name for g in gs.ghosts])
    # print(gs.path_to_corner(5, 5))

    from src.parsing.models import GameConfig
    gs = GameState(GameConfig())
    gs.switch_invincible()
    print('sans mode triche :', gs.invincible)
    gs.switch_cheat_mode()
    print('mode triche :', gs.cheat_mode)
    gs.switch_invincible()
    print('invincible :', gs.invincible)
    gs.switch_invincible()
    print('invincible :', gs.invincible)
    gs.switch_speed_pacman()
    print('vitesse :', gs.pacman.speed)
    gs.switch_speed_pacman()
    print('vitesse :', gs.pacman.speed)
    gs.switch_cheat_mode()
    print('mode triche :', gs.cheat_mode)
