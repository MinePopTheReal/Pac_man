from src.entity import (Speedy, Shadow, Bashful, Pokey,
                        Pacman, Direction, Ghost, GhostState)
from src.maze import Grid, CellContents
from src.parsing.models import GameConfig
from src.game_state.collision import collides
from src.maze.loader import generate_maze
from src.game_state.movement import (is_on_cell, advance, direction_home)
from src.game_state.cheats import Cheats
from src.game_state.direction_ghost import direction_toward
from enum import Enum, auto


# Speeds are in cells per second.
PACMAN_SPEED = 4.0

GHOST_SPEED = 3.0
# Cheat: Pac-Man speed is multiplied by this.
SPEED_MULTIPLIER = 2.0
# Cheat: ghost speed is multiplied by this.
SPEED_REDUCTION = 0.5
# Ghost speed is multiplied by this while it can be eaten (HUNTED)...
HUNTED_SPEED_FACTOR = 0.5
# ... and by this while it goes back to its corner (EATEN).
EATEN_SPEED_FACTOR = 2.0


class GameStatus(Enum):
    """State of the game, read by the screens to know what to display.

    DYING means Pac-Man has just been caught: the game waits for the
    death animation, which ends with GameState.end_death().
    """
    PLAYING = auto()
    DYING = auto()
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
        when status is DYING:
            play the death animation, then call game.end_death()
            (the game waits until end_death() is called)

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
        status (GameStatus): PLAYING, DYING, PAUSED, LOST or WON.
        previous_status (GameStatus): The status before the last pause,
            given back when the game is resumed.
        cheats (Cheats): Which cheats are on, for example
            cheats.enabled or cheats.invincible.
        started (bool): False until Pac-Man makes his first move in this
            level or after a lost life; ghosts and the level timer wait
            until then (useful to show a "Ready!" message).

    Positions are (y, x) = (row, column) in cells, not pixels: multiply
    by the tile size to draw, and swap to (x, y) for the screen.
    """
    def __init__(self, config: GameConfig) -> None:
        """Start a new game at level 1.

        Args:
            config (GameConfig): The game settings read from config.json.
        """
        self.config: GameConfig = config
        self.level: int = 1
        self.started: bool = False
        self.grid: Grid = self._new_grid()
        self.lives: int = self.config.lives
        self.cheats: Cheats = Cheats()
        self.level_time_left: float = float(self.config.level_max_time)
        self.time_hunt_ghosts: float = 0.0
        self.eaten_ghosts: int = 0
        self.score: int = 0
        self.wanted_direction: Direction = Direction.NONE
        self.status: GameStatus = GameStatus.PLAYING
        self.previous_status: GameStatus = GameStatus.PLAYING
        self.pacman = self._spawn_pacman()
        self.ghosts = self._spawn_ghosts()
        self.corner_maps: list[list[list[int]]] = self._maps_for_corners()
        self.pacman_map_cell: tuple[int, int] = (-1, -1)
        self.pacman_map: list[list[int]] = []
        self._update_pacman_map()

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
        classes: list[type[Ghost]] = [Shadow, Pokey, Bashful, Speedy]

        for classe, corner in zip(classes, self.grid.corners_grid):
            y, x = corner
            ghost = classe(Direction.NONE, (float(y), float(x)),
                           GhostState.HUNTER, GHOST_SPEED)
            lst_ghosts.append(ghost)
        return lst_ghosts

    def _reset_position(self) -> None:
        """Put every character back at its start, after a life is lost.

        Pac-Man goes back to the center and the ghosts to their corners as
        HUNTER. The super-pacgum effect is stopped, and the ghosts wait
        again for Pac-Man's first move. Pac-Man's speed is kept, so the
        speed cheat stays on.
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
        self.started = False

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
        self.pacman_map_cell = (-1, -1)
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

        - HUNTER: Pac-Man loses a life (not if invincible) and the game
          goes to DYING; what happens next is done by end_death().
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
                    self._start_death()
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
                dy, dx = ghost.direction.value
                ghost.direction = Direction((-dy, -dx))

    def _start_death(self) -> None:
        """Put the game in DYING and wait for end_death()."""
        self.status = GameStatus.DYING

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
        """Count down the level time; when it runs out, Pac-Man dies.

        All lives are lost and the game goes to DYING, so the death
        animation is played before the game is LOST.

        Args:
            dt (float): Seconds since the last frame.
        """
        self.level_time_left -= dt
        if self.level_time_left <= 0:
            self.level_time_left = 0.0
            self.lives = 0
            self._start_death()

    def _update_pacman_map(self) -> None:
        """Recompute the distance map to Pac-Man when he reaches a new cell.

        Ghosts use this map to chase or flee from Pac-Man.
        """
        py, px = self.pacman.position
        y = round(py)
        x = round(px)
        if self.pacman_map_cell != (y, x):
            self.pacman_map = self.grid.distances_from_cell(y, x)
            self.pacman_map_cell = (y, x)

    def _chase_map(self, ghost: Ghost,
                   corner_map: list[list[int]],
                   corner: tuple[int, int]) -> list[list[int]]:
        """Give the distance map a hunting ghost should follow.

        The map leads to the ghost's own target (see position_target). If
        that target cannot be reached (for example a cell of the '42'),
        the ghost aims at Pac-Man instead.

        Args:
            ghost (Ghost): A HUNTER ghost standing on a cell.
            corner_map (list[list[int]]): Distance map of its corner.
            corner (tuple[int, int]): Its corner.

        Returns:
            list[list[int]]: The distance map to follow.
        """
        shad_y, shad_x = self.ghosts[0].position
        target = ghost.position_target(self.pacman_map_cell,
                                       self.pacman.direction,
                                       (round(shad_y), round(shad_x)),
                                       corner)
        ty, tx = target
        ty = min(max(ty, 0), self.grid.height - 1)
        tx = min(max(tx, 0), self.grid.width - 1)

        if (ty, tx) == self.pacman_map_cell:
            return self.pacman_map

        if (ty, tx) == corner:
            return corner_map

        gy, gx = ghost.position
        map_toward_target = self.grid.distances_from_cell(ty, tx)

        if map_toward_target[int(gy)][int(gx)] == -1:
            return self.pacman_map
        return map_toward_target

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

    def switch_pause(self) -> None:
        """Pause the game, or resume it if it is paused.

        Call it when the pause key is pressed. While paused, nothing
        moves and the timers stop. Resuming gives back the status the
        game had before the pause (PLAYING or DYING), so a pause during
        Pac-Man's death puts the death animation on hold. It does
        nothing when the game is over (LOST or WON), so a finished game
        cannot be resumed.
        """
        if self.status in (GameStatus.PLAYING, GameStatus.DYING):
            self.previous_status = self.status
            self.status = GameStatus.PAUSED
        elif self.status == GameStatus.PAUSED:
            self.status = self.previous_status

    def select_direction(self, direction: Direction) -> None:
        """Tell which way the player wants Pac-Man to go.

        Call it when an arrow key (or WASD) is pressed. Pac-Man turns as
        soon as he can: if there is a wall, he keeps going straight and
        turns at the next opening.

        Args:
            direction (Direction): UP, DOWN, LEFT or RIGHT.
        """
        self.wanted_direction = direction

    def end_death(self) -> None:
        """Tell the game that the death animation is over.

        Call it once, when Pac-Man's death animation has finished. If
        lives are left, everybody goes back to the start and the game
        goes on (it waits for the first key press); otherwise the game
        is LOST. It does nothing if the status is not DYING.
        """
        if self.status != GameStatus.DYING:
            return
        if self.lives == 0:
            self.status = GameStatus.LOST
        else:
            self._reset_position()
            self.status = GameStatus.PLAYING

    def _ghost_wanted(self, ghost: Ghost, corner_map: list[list[int]],
                      corner: tuple[int, int]) -> Direction:
        """Choose where a ghost wants to go, depending on its state.

        EATEN ghosts go back to their corner, HUNTED ghosts run away from
        Pac-Man, and HUNTER ghosts go to their own target. Between two
        cells, the ghost keeps its direction.

        Args:
            ghost (Ghost): The ghost.
            corner_map (list[list[int]]): Distance map of its corner.
            corner (tuple[int, int]): Its corner.

        Returns:
            Direction: The direction the ghost wants to take.
        """
        if not is_on_cell(ghost.position):
            return ghost.direction

        y, x = ghost.position
        if ghost.state == GhostState.EATEN:
            return direction_home(int(y), int(x), corner_map, self.grid)
        if ghost.state == GhostState.HUNTED:
            return direction_toward(self.grid, int(y), int(x), ghost.direction,
                                    self.pacman_map, True)
        chase_map = self._chase_map(ghost, corner_map, corner)
        return direction_toward(self.grid, int(y), int(x), ghost.direction,
                                chase_map, False)

    def _pacman_eats(self) -> bool:
        """Eat what is on Pac-Man's cell and add the points.

        A super-pacgum also makes the ghosts edible. When the last pacgum
        is eaten, the game goes to the next level.

        Returns:
            bool: True if the level changed, so the frame must stop here.
        """
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
                return True
        return False

    def _ghost_speed(self, ghost: Ghost) -> float:
        """Compute the speed of a ghost from its state and the cheats.

        The speed is recomputed every frame, so it always matches the
        current state: slower while HUNTED, faster while EATEN, and
        twice as slow for every ghost with the slow ghosts cheat.

        Args:
            ghost (Ghost): The ghost.

        Returns:
            float: Its speed, in cells per second.
        """
        speed = GHOST_SPEED
        if ghost.state == GhostState.HUNTED:
            speed *= HUNTED_SPEED_FACTOR
        elif ghost.state == GhostState.EATEN:
            speed *= EATEN_SPEED_FACTOR
        if self.cheats.slow:
            speed *= SPEED_REDUCTION
        return speed

    def _move_ghosts(self, dt: float) -> None:
        """Move every ghost for one frame, unless they are frozen (cheat).

        Args:
            dt (float): Seconds since the last frame.
        """
        if not self.cheats.ghosts_frozen:
            for ghost, corner_map, corner in zip(self.ghosts, self.corner_maps,
                                                 self.grid.corners_grid):
                wanted = self._ghost_wanted(ghost, corner_map, corner)
                ghost.speed = self._ghost_speed(ghost)
                advance(ghost, wanted, dt, self.grid)

    def update(self, dt: float) -> None:
        """Move the game forward by one frame. Call it once per frame.

        Moves Pac-Man and the ghosts, eats pacgums, handles collisions,
        timers, the next level and the end of the game. Does nothing when
        the status is not PLAYING (for example during a pause). Ghosts
        and the level timer wait until Pac-Man makes his first move.

        Args:
            dt (float): Seconds since the last frame (about 0.016 at 60 FPS).
        """
        if self.status != GameStatus.PLAYING:
            return

        if not self.started:
            if self.wanted_direction != Direction.NONE:
                self.started = True
            else:
                return

        self._update_level_timer(dt)
        if self.status != GameStatus.PLAYING:
            return

        advance(self.pacman, self.wanted_direction, dt, self.grid)

        if self._pacman_eats():
            return

        self._update_pacman_map()

        self._move_ghosts(dt)

        self._update_time_ghost_hunt(dt)
        self._update_respawn_ghost(dt)
        self._check_ghost_collision()
