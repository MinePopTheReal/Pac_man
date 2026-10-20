from src.utils.sprite_sheet_manager import SpriteSheetManager, Rotation
from src.game_state.game_state import GameState, Direction, GameConfig
from src.rendering.entities_renderer import EntitiesRenderer
from src.rendering.wall_renderer import WallRenderer
from src.parsing.parse_config import ConfigParser
from src.rendering.layer import Layer

from pyglet import window, gl, display, clock, app
from pyglet.window import key


class Display(window.Window):
    def __init__(self, game_state: GameState):

        # Spritesheets
        self.wall_spritesheet = SpriteSheetManager(
            "assets/wall_spritesheet_config.json",
            "assets/wall_spritesheet.png",
            "RGB",
            
        )
        self.entities_spritesheet = SpriteSheetManager(
            "assets/entities_spritesheet_config.json",
            "assets/entities_spritesheet.png",
            "RGBA"
        )

        # Display config
        display_data = display.get_display()
        screen = display_data.get_default_screen()

        super().__init__(width=screen.width - 100, height=screen.height - 100, caption="Pac-Man")

        self._current_level = -1

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # Config

        self.game_state = game_state

        # Buffer
        initial_maze_width = self.game_state.config.width * \
            self.wall_spritesheet.spritesheet_config.tile_size * \
            3

        initial_maze_height = self.game_state.config.height * \
            self.wall_spritesheet.spritesheet_config.tile_size * \
            3

        self.zoom = max(1, min(
                screen.width // initial_maze_width,
                screen.height // initial_maze_height
            ))

        self.wall_spritesheet.preloading_sprites(
            [Rotation.R0, Rotation.R90, Rotation.R180, Rotation.R270],
            self.zoom)
        self.entities_spritesheet.preloading_sprites(
            [Rotation.R0],
            self.zoom
        )

        self.maze_width = initial_maze_width * self.zoom
        self.maze_height = initial_maze_height * self.zoom

        self.maze_pitch = self.maze_width * self.wall_spritesheet.bytes_number_per_pixel
        self.entities_pitch = self.maze_width * self.entities_spritesheet.bytes_number_per_pixel

        self.wall_layer = Layer(self.maze_width, self.maze_height, self.wall_spritesheet.format)
        self.entities_layer = Layer(self.maze_width, self.maze_height, self.entities_spritesheet.format)

        self.wall_renderer = WallRenderer(self.wall_spritesheet)
        self.entities_renderer = EntitiesRenderer(
            self.game_state,
            self.entities_layer,
            self.entities_spritesheet,
            self.wall_spritesheet.spritesheet_config.tile_size,
            self.wall_spritesheet.bytes_number_per_pixel,
            self.zoom
        )

        self.maze_pos_x = self.width // 2 - self.maze_width // 2
        self.maze_pos_y =  self.height // 2 - self.maze_height // 2

        self.direction_input = {
            key.W: Direction.UP,
            key.D: Direction.RIGHT,
            key.S: Direction.DOWN,
            key.A: Direction.LEFT
        }

        clock.schedule_interval(self.entities_renderer.update_animation, 0.115)
        clock.schedule_interval(self.game_state.update, 0.01)

    def _build_maze(self):
        self.wall_renderer.create_maze_render(self.game_state.grid.cells, self.wall_layer.buffer_view, self.zoom)
        self.curr_level = self.game_state.level

    def on_key_press(self, symbol, modifiers):
        direction = self.direction_input.get(symbol)
        if direction is not None:
            self.game_state.wanted_direction = direction

    def on_draw(self):
        self.clear()
        if self._current_level != self.game_state.level:
            self._build_maze()
        self.wall_layer.draw(self.maze_pos_x, self.maze_pos_y)
        self.entities_layer.draw(self.maze_pos_x, self.maze_pos_y)

        self.entities_renderer.draw_entities()


config = ConfigParser().load_config("config.json", GameConfig)
game_state = GameState(config)

render = Display(game_state)

app.run()
