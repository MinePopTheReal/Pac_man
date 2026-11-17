from src.rendering.entities_renderer import EntitiesRenderer
from src.rendering.sprite_sheet_manager import Rotation
from src.rendering.wall_renderer import WallRenderer
from src.rendering.widget.widget import Widget
from src.game.game_state import GameState
from src.parsing.models import GameConfig
from src.rendering.assets import Assets
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
        wall_size: int,
        entity_size: int,
        x: int,
        y: int
    ) -> None:

        self.wall_size = wall_size
        self.entity_size = entity_size

        width = config.width * TILES_PER_CELL * wall_size
        height = config.height * TILES_PER_CELL * wall_size
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
            self.wall_size,
            self.entity_size,
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
            self.wall_size,
        )
        self.assets.entities_spritesheet.preloading_sprites(
            [Rotation.R0], self.entity_size
        )

    def _build_maze(self) -> None:
        """Draw the walls of the current level into the wall layer.

        Remembers the level that was drawn, so the walls are drawn again
        only when the level changes.
        """
        self.wall_renderer.create_maze_render(
            self.game_state.grid.cells,
            self.wall_layer.buffer_view,
            self.wall_size
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
