from src.utils.sprite_sheet_manager import SpriteSheetManager, Rotation
from src.game_state.game_state import GameState, Direction, GameStatus
from src.entity.ghost import GhostState
from src.maze.grid import CellContents
from src.rendering.layer import Layer
from src.rendering.sprites_name import (
    EYES_BY_DIRECTION,
    GHOSTS_BY_DIRECTION,
    PACGUM,
    SUPER_PACGUM,
    PACMAN_BY_DIRECTION,
    PACMAN_DEATH,
    GHOST_FEAR_BLUE,
    GHOST_FEAR_WHITE,
)


# Time remaining until the end of 'Hunted' for the ghosts to start flashing
FEAR_BLINK_TIME = 3
# Number of frames between each flash
FEAR_BLINK_PERIOD = 4
# Number of ticks before triggering the health loss animation
NUMBER_FREEZE_TICK = 5


class EntitiesRenderer:
    """
    This class is used to place each entity in the buffer and
    to update the animations and positions with each frame.
    """
    def __init__(
        self,
        game_state: GameState,
        layer: Layer,
        spritesheet: SpriteSheetManager,
        maze_tile_size: int,
        number_of_tiles_per_cell: int,
        zoom: int,
    ):
        self.zoom: int = zoom
        self.layer: Layer = layer
        self.game_state: GameState = game_state
        self.spritesheet: SpriteSheetManager = spritesheet
        self.number_of_tiles_per_cell: int = number_of_tiles_per_cell
        self.maze_tile_size: int = maze_tile_size

        self.offset_px = 4.5

        self.start_to_die: int = -1
        self.frame = 0
        self.previous_direction: Direction = Direction.NONE

    def _draw_sprite(
        self, sprite_name: str, maze_x: float, maze_y: float, frame: int = -1
    ) -> None:
        """
        Calculate the new coordinates of the entity in the buffer and add them
        to the buffer.

        Args:
            sprite_name (str): the sprite's name
            maze_x (float): the (x) coordinates on the maze
            maze_y (float): the (y) coordinates on the maze
            frame (int, optional): frame number (the frame's position in
            the animation). Defaults to -1.
        """
        new_x, new_y = (
            int(
                (
                    maze_x
                    * self.maze_tile_size
                    * self.number_of_tiles_per_cell
                    + self.offset_px
                )
                * self.zoom
            ),
            int(
                (
                    maze_y
                    * self.maze_tile_size
                    * self.number_of_tiles_per_cell
                    + self.offset_px
                )
                * self.zoom
            ),
        )

        self.spritesheet.copy_tile_into_buffer(
            self.layer.buffer_view,
            sprite_name,
            Rotation.R0,
            new_x,
            new_y,
            self.zoom,
            self.frame if frame == -1 else frame,
        )

    def _draw_pacman(self) -> None:
        """
        Manages Pac-Man's animations by determining the sprite name based on
        Pac-Man's state and adds it to the buffer.
        """
        direction = self.game_state.pacman.direction
        pos_y, pos_x = self.game_state.pacman.position
        frame = -1

        if (
            self.game_state.status == GameStatus.DYING
            and self._death_frame >= 0
        ):
            sprite_name = PACMAN_DEATH
            frame = min(
                self._death_frame,
                len(self.spritesheet.sprites_bytes[sprite_name][Rotation.R0])
                - 1,
            )

        elif (
            direction == Direction.NONE
            and self.previous_direction == Direction.NONE
        ):
            sprite_name = PACMAN_BY_DIRECTION[Direction.UP]
            frame = 2
        else:
            if direction != Direction.NONE:
                self.previous_direction = direction
            sprite_name = PACMAN_BY_DIRECTION[self.previous_direction]

        self._draw_sprite(sprite_name, pos_x, pos_y, frame)

    def _draw_ghosts(self) -> None:
        """
        Manages the ghosts' animations by assigning the sprite name based
        on their state and adds them to the buffer.
        """
        for ghost in self.game_state.ghosts:
            pos_y, pos_x = ghost.position

            if ghost.state == GhostState.HUNTED:
                blinking = (
                    self.game_state.time_hunt_ghosts <= FEAR_BLINK_TIME
                    and self.frame % FEAR_BLINK_PERIOD <= 1
                )
                sprite_name = GHOST_FEAR_WHITE if blinking else GHOST_FEAR_BLUE
            elif ghost.state == GhostState.EATEN:
                sprite_name = EYES_BY_DIRECTION[ghost.direction]
            else:
                sprite_name = GHOSTS_BY_DIRECTION[ghost.name][ghost.direction]

            self._draw_sprite(sprite_name, pos_x, pos_y)

    # TODO Modify this function once the pacgums are stored somewhere
    def _draw_pacgums(self) -> None:
        """
        Manages the sprites and animations for Pacgums
        """
        for y in range(len(self.game_state.grid.cells)):
            for x in range(len(self.game_state.grid.cells[y])):
                if (
                    self.game_state.grid.cells[y][x].content
                    == CellContents.PACGUM
                ):
                    sprite_name = PACGUM
                elif (
                    self.game_state.grid.cells[y][x].content
                    == CellContents.SUPER_PACGUM
                    and self.frame % 2 == 0
                ):
                    sprite_name = SUPER_PACGUM
                else:
                    continue
                self._draw_sprite(sprite_name, x, y)

    @property
    def _death_frame(self) -> int:
        """
        Allows you to obtain the frame from Pac-Man's death animation

        Returns:
            int: the frame number
        """
        if self.start_to_die == -1:
            return -NUMBER_FREEZE_TICK
        return self.frame - self.start_to_die - NUMBER_FREEZE_TICK

    def _update_death(self) -> None:
        """
        Manages Pac-Man's death animations and lets you
        restart the game once it's over
        """
        if self.start_to_die == -1:
            self.start_to_die = self.frame
        if (
            self._death_frame
            > len(self.spritesheet.sprites_bytes[PACMAN_DEATH][Rotation.R0])
            - 1
        ):
            self.game_state.end_death()
            self.previous_direction = Direction.NONE
            self.start_to_die = -1

    def update_animation(self, dt: float) -> None:
        """Increments the frame variable, which advances the entity's
        animation, and also triggers the death animation if necessary.

        Args:
            dt (float): time delta
        """
        self.frame += 1
        if self.game_state.status == GameStatus.DYING:
            self._update_death()

    def draw_entities(self) -> None:
        """
        Manages animations based on the game's status
        """
        self.layer.clear()
        if self.game_state.status == GameStatus.DYING:
            self._draw_pacgums()
            self._draw_pacman()

        elif self.game_state.status == GameStatus.PLAYING:
            self._draw_pacgums()
            self._draw_ghosts()
            self._draw_pacman()
