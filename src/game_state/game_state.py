from src.entity import (Speedy, Shadow, Bashful, Pokey,
                        Pacman, Direction, Ghost, GhostState)
from src.maze import Grid, CellContents, LST_DIRECTION
from src.parsing.models import GameConfig
from src.game_state.collision import collides
from src.maze.loader import generate_maze
from src.game_state.movement import (is_on_cell, advance, direction_home)
from src.game_state.cheats import Cheats
from enum import Enum, auto
import random


# Speeds are in cells per second.
PACMAN_SPEED = 4.0
# Cheat: Pac-Man speed is multiplied by this.
SPEED_MULTIPLIER = 2.0
# Cheat: ghost speed is multiplied by this.
SPEED_REDUCTION = 0.5
GHOST_SPEED = 3.0


class GameStatus(Enum):
    """State of the game, read by the screens to know what to display."""
    PLAYING = auto()
    PAUSED = auto()
    LOST = auto()
    WON = auto()


class GameState:
    """Everything about the game being played, and its rules.

    How to use it (main loop):
        game = GameState(config)
        every frame:
            game.select_direction(...)   when an arrow key is pressed
            game.switch_pause()          when the pause key is pressed
            game.update(dt)              dt = seconds since last frame
            then draw using the attributes below

    Attributes you can read to draw the game (do not change them):
        grid (Grid): The current maze; grid.get_all_cells() gives every
            (y, x, cell) with its walls and content.
        pacman (Pacman): position (y, x) in cells, direction.
        ghosts (list[Ghost]): position, direction and state of each
            ghost (HUNTER: normal, HUNTED: can be eaten, EATEN: going
            back to its corner).
        score (int): Current score.
        lives (int): Lives left.
        level (int): Current level, starting at 1.
        level_time_left (float): Seconds left in this level.
        time_hunt_ghosts (float): Seconds left while ghosts can be
            eaten, 0.0 when no super-pacgum effect is running.
        status (GameStatus): PLAYING, PAUSED, LOST or WON.
        cheats (Cheats): Which cheats are on, for example
            cheats.enabled or cheats.invincible.

    Positions are (y, x) = (row, column) in cells, not pixels: multiply
    by the tile size to draw, and swap to (x, y) for the screen.
    """
    def __init__(self, config: GameConfig) -> None:
        """Start a new game at level 1.

        Args:
            config (GameConfig): The game settings read from config.json.
        """
        self.config: GameConfig = config
        self.rng = random.Random()
        self.level: int = 1
        self.grid: Grid = self._new_grid()
        self.lives: int = self.config.lives
        self.cheats: Cheats = Cheats()
        self.level_time_left: float = float(self.config.level_max_time)
        self.time_hunt_ghosts: float = 0.0
        self.eaten_ghosts: int = 0
        self.score: int = 0
        self.wanted_direction: Direction = Direction.NONE
        self.status: GameStatus = GameStatus.PLAYING
        self.pacman = self._spawn_pacman()
        self.ghosts = self._spawn_ghosts()
        self.corner_maps: list[list[list[int]]] = self._maps_for_corners()

    def _spawn_pacman(self) -> Pacman:
        """Create Pac-Man in the middle of the maze.

        Returns:
            Pacman: Pac-Man, not moving yet.
        """
        y, x = self.grid.center_grid
        pacman = Pacman(Direction.NONE, (float(y), float(x)), PACMAN_SPEED)
        return pacman

    def _spawn_ghosts(self) -> list[Ghost]:
        """Create the 4 ghosts, one in each corner.

        The order matches grid.corners_grid: top left, top right, bottom
        left, bottom right.

        Returns:
            list[Ghost]: The 4 ghosts, all HUNTER.
        """
        lst_ghosts: list[Ghost] = []
        classes = [Shadow, Pokey, Bashful, Speedy]

        for classe, corner in zip(classes, self.grid.corners_grid):
            y, x = corner
            ghost = classe(Direction.NONE, (float(y), float(x)),
                           GhostState.HUNTER, GHOST_SPEED)
            lst_ghosts.append(ghost)
        return lst_ghosts

    def _reset_position(self) -> None:
        """Put every character back at its start, after a life is lost.

        Pac-Man goes back to the center and the ghosts to their corners as
        HUNTER. The super-pacgum effect is stopped. Speeds are kept, so the
        speed cheats stay on.
        """
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
        """Generate the maze of the current level.

        Level 1 uses the seed of the config, the next levels are random.

        Returns:
            Grid: The new maze.
        """
        seed = self.config.seed if self.level == 1 else 0
        return generate_maze(self.config.height, self.config.width, seed,
                             self.config.pacgum)

    def _build_level(self) -> None:
        """Prepare the current level: new maze, characters back in place.

        Score, lives and cheats are kept.
        """
        self.grid = self._new_grid()
        self.corner_maps = self._maps_for_corners()
        self._reset_position()
        self.level_time_left = float(self.config.level_max_time)
        self.eaten_ghosts = 0

    def _next_level(self) -> None:
        """Go to the next level, or win the game after the last one."""
        if self.level < self.config.nb_level:
            self.level += 1
            self._build_level()
        else:
            self.status = GameStatus.WON

    def _maps_for_corners(self) -> list[list[list[int]]]:
        """Compute, for each corner, the distance of every cell to it.

        Eaten ghosts use these maps to go back to their corner. The order
        matches the ghosts list.

        Returns:
            list[list[list[int]]]: One distance map per corner.
        """
        lst_maps: list[list[list[int]]] = []
        for corner in self.grid.corners_grid:
            y, x = corner
            lst_maps.append(self.grid.distances_from_cell(y, x))
        return lst_maps

    def _check_ghost_collision(self) -> None:
        """Apply what happens when Pac-Man touches a ghost.

        - HUNTER: Pac-Man loses a life (not if invincible) and everybody
          goes back to its start; the game is LOST at 0 lives.
        - HUNTED: the ghost is eaten and goes back to its corner. Points
          double for each ghost eaten with the same super-pacgum
          (200, 400, 800, 1600 with the default config).
        - EATEN: nothing happens.
        """
        for ghost in self.ghosts:
            if ghost.state == GhostState.HUNTER:
                if collides(self.pacman.position, ghost.position):
                    if self.cheats.invincible:
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
        """Start the super-pacgum effect: HUNTER ghosts become HUNTED."""
        self.time_hunt_ghosts = self.config.timer_hunt_ghosts
        for ghost in self.ghosts:
            if ghost.state == GhostState.HUNTER:
                ghost.state = GhostState.HUNTED

    def _update_time_ghost_hunt(self, dt: float) -> None:
        """Count down the super-pacgum effect; at the end, ghosts hunt again.

        Args:
            dt (float): Seconds since the last frame.
        """
        if self.time_hunt_ghosts > 0:
            self.time_hunt_ghosts -= dt
            if self.time_hunt_ghosts <= 0:
                self.time_hunt_ghosts = 0.0
                for ghost in self.ghosts:
                    if ghost.state == GhostState.HUNTED:
                        ghost.state = GhostState.HUNTER

    def _update_respawn_ghost(self, dt: float) -> None:
        """Count down the wait of eaten ghosts that reached their corner.

        When the wait is over, the ghost becomes HUNTER again.

        Args:
            dt (float): Seconds since the last frame.
        """
        for ghost, corner in zip(self.ghosts, self.grid.corners_grid):
            if ghost.state == GhostState.EATEN and ghost.position == corner:
                ghost.respawn_timer -= dt
                if ghost.respawn_timer <= 0:
                    ghost.respawn_timer = 0.0
                    ghost.state = GhostState.HUNTER

    def _update_level_timer(self, dt: float) -> None:
        """Count down the level time; when it runs out, the game is LOST.

        Args:
            dt (float): Seconds since the last frame.
        """
        self.level_time_left -= dt
        if self.level_time_left <= 0:
            self.level_time_left = 0.0
            self.status = GameStatus.LOST

    def switch_cheat_mode(self) -> None:
        """Turn the cheat mode on or off.

        The other cheat methods do nothing while the cheat mode is off.
        Cheats already on stay on when the cheat mode is turned off.
        """
        self.cheats.enabled = not self.cheats.enabled

    def switch_invincible(self) -> None:
        """Cheat: turn invincibility on or off (ghosts cannot kill Pac-Man)."""
        if self.cheats.enabled:
            self.cheats.invincible = not self.cheats.invincible

    def switch_ghosts_frozen(self) -> None:
        """Cheat: stop or restart the ghosts."""
        if self.cheats.enabled:
            self.cheats.ghosts_frozen = not self.cheats.ghosts_frozen

    def skip_level(self) -> None:
        """Cheat: finish the current level at once (wins after the last)."""
        if self.cheats.enabled:
            self._next_level()

    def add_extra_life(self) -> None:
        """Cheat: give Pac-Man one more life."""
        if self.cheats.enabled:
            self.lives += 1

    def switch_speed_pacman(self) -> None:
        """Cheat: make Pac-Man twice as fast, or back to normal speed."""
        if self.cheats.enabled:
            self.cheats.fast = not self.cheats.fast
            if self.cheats.fast:
                self.pacman.speed = PACMAN_SPEED * SPEED_MULTIPLIER
            else:
                self.pacman.speed = PACMAN_SPEED

    def switch_slow_ghosts(self) -> None:
        """Cheat: make the ghosts twice as slow, or back to normal speed."""
        if self.cheats.enabled:
            self.cheats.slow = not self.cheats.slow
            if self.cheats.slow:
                for ghost in self.ghosts:
                    ghost.speed = GHOST_SPEED * SPEED_REDUCTION
            else:
                for ghost in self.ghosts:
                    ghost.speed = GHOST_SPEED

    def switch_pause(self) -> None:
        """Pause the game, or resume it if it is paused.

        Call it when the pause key is pressed. While paused, nothing
        moves and the timers stop. It does nothing when the game is
        over (LOST or WON), so a finished game cannot be resumed.
        """
        if self.status == GameStatus.PLAYING:
            self.status = GameStatus.PAUSED
        elif self.status == GameStatus.PAUSED:
            self.status = GameStatus.PLAYING

    def select_direction(self, direction: Direction) -> None:
        """Tell which way the player wants Pac-Man to go.

        Call it when an arrow key (or WASD) is pressed. Pac-Man turns as
        soon as he can: if there is a wall, he keeps going straight and
        turns at the next opening.

        Args:
            direction (Direction): UP, DOWN, LEFT or RIGHT.
        """
        self.wanted_direction = direction

    def update(self, dt: float) -> None:
        """Move the game forward by one frame. Call it once per frame.

        Moves Pac-Man and the ghosts, eats pacgums, handles collisions,
        timers, the next level and the end of the game. Does nothing when
        the status is not PLAYING (for example during a pause).

        Args:
            dt (float): Seconds since the last frame (about 0.016 at 60 FPS).
        """
        if self.status != GameStatus.PLAYING:
            return

        self._update_level_timer(dt)
        if self.status == GameStatus.LOST:
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

        if not self.cheats.ghosts_frozen:
            for ghost, maze in zip(self.ghosts, self.corner_maps):
                y, x = ghost.position
                if ghost.state == GhostState.EATEN:
                    if is_on_cell((y, x)):
                        wanted = direction_home(int(y), int(x), maze,
                                                self.grid)
                    else:
                        wanted = ghost.direction
                else:
                    wanted = self.rng.choice(LST_DIRECTION)
                advance(ghost, wanted, dt, self.grid)
        self._update_time_ghost_hunt(dt)
        self._update_respawn_ghost(dt)
        self._check_ghost_collision()
