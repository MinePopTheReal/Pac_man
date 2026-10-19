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
    GHOST_FEAR_WHITE
)
from numpy import ndarray
from pyglet import image


class EntitiesRenderer:
    def __init__(
        self,
        game_state: GameState,
        layer: Layer,
        spritesheet: SpriteSheetManager,
        maze_tile_size: int,
        number_of_tiles_per_cell: int,
        zoom: int
    ):

        self.zoom: int = zoom
        self.layer: Layer = layer
        self.game_state: GameState = game_state
        self.spritesheet: SpriteSheetManager = spritesheet
        self.number_of_tiles_per_cell: int = number_of_tiles_per_cell
        self.maze_tile_size: int = maze_tile_size

        self.offset_px = 4.5

        self.frame = 0
        self.previous_direction: Direction = Direction.NONE

    def _draw_sprite(self, sprite_name: str, maze_x: float, maze_y: float, frame: int = -1) -> None:
        new_x, new_y = (
            int((maze_x * self.maze_tile_size * self.number_of_tiles_per_cell + self.offset_px) * self.zoom),
            int((maze_y  * self.maze_tile_size * self.number_of_tiles_per_cell + self.offset_px) * self.zoom)
        )

        self.spritesheet.copy_tile_into_buffer(
            self.layer.buffer_view,
            sprite_name,
            Rotation.R0,
            new_x,
            new_y,
            self.zoom,
            self.frame if frame == -1 else frame
        )

    def _draw_pacman(self):
        direction = self.game_state.pacman.direction
        pos_y, pos_x = self.game_state.pacman.position
        frame = -1

        if direction == Direction.NONE:
            if self.previous_direction == Direction.NONE:
                sprite_name = PACMAN_BY_DIRECTION[Direction.UP]
                frame = 2
            else:
                sprite_name = PACMAN_BY_DIRECTION[self.previous_direction]
        else:
            self.previous_direction = direction
            sprite_name = PACMAN_BY_DIRECTION[direction]
        self._draw_sprite(sprite_name, pos_x, pos_y, frame)

    def _draw_ghosts(self):
        for ghost in self.game_state.ghosts:
            direction = ghost.direction
            pos_y, pos_x = ghost.position

            if ghost.state == GhostState.HUNTER:
                if direction == Direction.NONE:
                    sprite_name = GHOSTS_BY_DIRECTION[ghost.name][Direction.UP]
                else:
                    sprite_name = GHOSTS_BY_DIRECTION[ghost.name][direction]

            elif ghost.state == GhostState.HUNTED:
                if self.game_state.time_hunt_ghosts <= 3.0 and self.frame % 4 <= 1:
                    sprite_name = GHOST_FEAR_WHITE
                else:
                    sprite_name = GHOST_FEAR_BLUE

            elif ghost.state == GhostState.EATEN:
                if direction == Direction.NONE:
                    sprite_name = EYES_BY_DIRECTION[Direction.UP]
                else:
                    sprite_name = EYES_BY_DIRECTION[direction]

            self._draw_sprite(sprite_name, pos_x, pos_y)

    def _draw_pacgums(self):
        for y in range(len(self.game_state.grid.cells)):
            for x in range(len(self.game_state.grid.cells[y])):
                if self.game_state.grid.cells[y][x].content == CellContents.PACGUM:
                    sprite_name = PACGUM
                elif self.game_state.grid.cells[y][x].content == CellContents.SUPER_PACGUM and self.frame % 2 == 0:
                    sprite_name = SUPER_PACGUM
                else:
                    continue
                self._draw_sprite(sprite_name, x, y)

    def update_animation(self, dt):
        self.frame += 1

    def draw_entities(self):
        self.layer.clear()

        if self.game_state.status == GameStatus.PLAYING:
            self._draw_pacgums()
            self._draw_ghosts()
            self._draw_pacman()

