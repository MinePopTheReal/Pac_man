from src.rendering.assets import Assets, WALL_SIZE, ENTITIES_SIZE
from src.rendering.entities_renderer import EntitiesRenderer
from src.rendering.wall_renderer import WallRenderer
from src.utils.sprite_sheet_manager import Rotation
from src.game_state.game_state import GameState
from src.utils.widget.widget import Widget
from src.parsing.models import GameConfig
from src.rendering.layer import Layer


from pyglet import clock, gl


TILES_PER_CELL = 3
ANIMATION_INTERVAL_S = 0.115


class MazeView(Widget):
    def __init__(
        self,
        game_state: GameState,
        assets: Assets,
        config: GameConfig,
        x: int,
        y: int,
    ) -> None:
        width = config.width * TILES_PER_CELL * WALL_SIZE
        height = config.height * TILES_PER_CELL * WALL_SIZE
        super().__init__(width, height, x=x, y=y, anchor_x=0.5, anchor_y=0.5)

        self.game_state = game_state
        self.assets = assets
        self._current_level = -1

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

    def start_animation(self) -> None:
        clock.schedule_interval(
            self.entities_renderer.update_animation, ANIMATION_INTERVAL_S
        )

    def stop_animation(self) -> None:
        clock.unschedule(self.entities_renderer.update_animation)

    def _preload_sprites(self) -> None:
        self.assets.wall_spritesheet.preloading_sprites(
            [Rotation.R0, Rotation.R90, Rotation.R180, Rotation.R270],
            WALL_SIZE,
        )
        self.assets.entities_spritesheet.preloading_sprites(
            [Rotation.R0], ENTITIES_SIZE
        )

    def _build_maze(self) -> None:
        self.wall_renderer.create_maze_render(
            self.game_state.grid.cells, self.wall_layer.buffer_view, WALL_SIZE
        )
        self._current_level = self.game_state.level
        self.wall_layer.is_dirty()

    def _render(self) -> None:
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        if self._current_level != self.game_state.level:
            self._build_maze()
        self.wall_layer.draw(self.left, self.bottom)
        self.entities_renderer.draw_entities()
        self.entities_layer.draw(self.left, self.bottom)
