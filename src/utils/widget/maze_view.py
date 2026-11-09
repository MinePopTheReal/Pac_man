from src.rendering.assets import Assets, WALL_SIZE, ENTITIES_SIZE
from src.rendering.entities_renderer import EntitiesRenderer
from src.rendering.wall_renderer import WallRenderer
from src.utils.sprite_sheet_manager import Rotation
from src.game_state.game_state import GameState
from src.utils.widget.widget import Widget
from src.parsing.models import GameConfig
from src.rendering.layer import Layer


from pyglet import gl


TILES_PER_CELL = 3
ANIMATION_INTERVAL_S = 0.115

MAX_CATCH_UP_S = 0.25


class MazeView(Widget):
    """Widget that draws the maze, the pacgums and the characters.

    The walls are drawn into a first layer, only when a new level starts.
    The pacgums, Pac-Man and the ghosts are drawn into a second layer,
    on top of the walls, at each frame. The size of the widget depends on
    the size of the maze in the config.
    """
    def __init__(
        self,
        game_state: GameState,
        assets: Assets,
        config: GameConfig,
        x: int,
        y: int,
        # hud_height: int
    ) -> None:

        width = config.width * TILES_PER_CELL * WALL_SIZE
        height = config.height * TILES_PER_CELL * WALL_SIZE
        # hud_height =

        # wall_size = min(self.assets.window_width //
        # (3*width), self.assets.window_height - hud_height -// (3*height))
        super().__init__(width, height, x=x, y=y, anchor_x=0.5, anchor_y=0.5)

        self.game_state = game_state
        self.assets = assets

        self._current_level = -1
        self._anim_time = 0.0

        self._preload_sprites()

        self.wall_layer = Layer(width, height, assets.wall_spritesheet.format)
        self.entities_layer = Layer(
            width, height, assets.entities_spritesheet.format
        )

        self.wall_renderer = WallRenderer(assets.wall_spritesheet)
        self.entities_renderer = EntitiesRenderer(
            game_state,
            self.entities_layer,
            assets.entities_spritesheet,
            assets.wall_spritesheet.bytes_number_per_pixel,
            ENTITIES_SIZE,
        )

    def update(self, dt: float) -> None:
        """Make the animation of the characters move forward.

        The animation advances by one step every ANIMATION_INTERVAL_S
        seconds, whatever the frame rate. It does not move the game
        itself: that is done by the game state.

        Args:
            dt (float): Seconds since the last frame.
        """
        self._anim_time += min(dt, MAX_CATCH_UP_S)
        while self._anim_time >= ANIMATION_INTERVAL_S:
            self._anim_time -= ANIMATION_INTERVAL_S
            self.entities_renderer.update_animation(ANIMATION_INTERVAL_S)

    def _preload_sprites(self) -> None:
        """Prepare the sprites at the size used on screen.

        The walls are prepared in the four rotations, the entities in
        their normal orientation, so they are not computed again while
        the game is running.
        """
        self.assets.wall_spritesheet.preloading_sprites(
            [Rotation.R0, Rotation.R90, Rotation.R180, Rotation.R270],
            WALL_SIZE,
        )
        self.assets.entities_spritesheet.preloading_sprites(
            [Rotation.R0], ENTITIES_SIZE
        )

    def _build_maze(self) -> None:
        """Draw the walls of the current level into the wall layer.

        Remembers the level that was drawn, so the walls are drawn again
        only when the level changes.
        """
        self.wall_renderer.create_maze_render(
            self.game_state.grid.cells, self.wall_layer.buffer_view, WALL_SIZE
        )
        self._current_level = self.game_state.level
        self.wall_layer.mark_dirty()

    def _render(self) -> None:
        """Draw the maze in the window.

        If a new level has started, the walls are drawn again first.
        Then the layer of the walls is drawn, and the layer of the
        entities (pacgums and characters) on top of it, with
        transparency.
        """
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        if self._current_level != self.game_state.level:
            self._build_maze()
        self.wall_layer.draw(self.left, self.bottom)
        self.entities_renderer.draw_entities()
        self.entities_layer.draw(self.left, self.bottom)
