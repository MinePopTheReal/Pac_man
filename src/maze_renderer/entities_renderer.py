from pyglet import window, app, sprite, image, clock, display
from src.maze_renderer.wall_renderer import WallRenderer
from src.maze.loader import generate_maze
from src.game_state.game_state import GameState, Direction, GameStatus
from src.parsing.parse_config import ConfigParser
from src.parsing.models import GameConfig, Spritesheet
from src.utils.sprite_sheet_manager import SpriteSheetManager, Rotation
from pyglet.window import key
from pyglet import gl
from math import floor
from src.entity.ghost import GhostState
from src.maze.grid import CellContents
from numpy import frombuffer, uint8, ndarray


from dataclasses import dataclass

@dataclass
class CharactersSprites():
    sprites_for_direction: dict[Direction, str]

@dataclass
class PacManSprites():
    normal: CharactersSprites
    death: str

@dataclass
class GhostsSprites():
    normal: CharactersSprites
    death: CharactersSprites
    fear_blue: str
    fear_white: str

@dataclass
class PacGumSprites():
    super_pacgum: str
    pacgum: str
    

class EntitiesRenderer:
    def __init__(self, game_state: GameState, buffer_view: ndarray, buffer_pitch: int, spritesheet: SpriteSheetManager, zoom: int):

        self.game_state = game_state

        self.spritesheet = spritesheet

        self.zoom = zoom

        self.pacman_sprites_name = self.load_pacman_sprites()
        self.pacgums_sprites_name = self.load_pacgums_sprites()
        self.ghosts_sprites_name = self.load_ghosts_sprites()

        self.buffer_view: ndarray = buffer_view
        self.buffer_pitch: int = buffer_pitch

        self.previous_direction: Direction = Direction.NONE

        self.frame = 0

    def load_pacman_sprites(self):
        return PacManSprites(
            normal=CharactersSprites({
                Direction.UP: "pacman_top",
                Direction.RIGHT: "pacman_right",
                Direction.DOWN: "pacman_bottom",
                Direction.LEFT: "pacman_left"
            }),
            death="pacman_death"
        )

    def load_ghosts_sprites(self):
        normal_sprite: dict[str, list[str]] = {
            "blinky": [
                "blinky_top",
                "blinky_right",
                "blinky_bottom",
                "blinky_left"
                ],
            "pinky": [
                "pinky_top",
                "pinky_right",
                "pinky_bottom",
                "pinky_left"
                ],
            "inky": [
                "inky_top",
                "inky_right",
                "inky_bottom",
                "inky_left"
                ],
            "clyde": [
                "clyde_top",
                "clyde_right",
                "clyde_bottom",
                "clyde_left"
                ]
        }

        loaded_sprites: dict[str, GhostsSprites] = {}

        for ghost_name, sprite_name in normal_sprite.items():
            loaded_sprites[ghost_name] = GhostsSprites(
                normal=CharactersSprites({
                    Direction.UP: sprite_name[0],
                    Direction.RIGHT: sprite_name[1],
                    Direction.DOWN: sprite_name[2],
                    Direction.LEFT: sprite_name[3]
                }),
                death=CharactersSprites({
                    Direction.UP: "ghosts_eyes_top",
                    Direction.RIGHT: "ghosts_eyes_right",
                    Direction.DOWN: "ghosts_eyes_bottom",
                    Direction.LEFT: "ghosts_eyes_left"
                }),
                fear_blue="ghosts_fear_blue",
                fear_white="ghosts_fear_white"
            )
        return loaded_sprites

    def load_pacgums_sprites(self):
        return PacGumSprites(
            super_pacgum="super_pacgum",
            pacgum="pacgum"
        )

    def update_sprite(self, sprite_name: str, maze_x: float, maze_y: float, frame: int = -1) -> None:
        new_x, new_y = int((maze_x * 8 * 3 + 4.5) * self.zoom), int((maze_y  * 8 * 3 + 4.5) * self.zoom)

        self.spritesheet.copy_tile_into_buffer(
            self.buffer_view,
            sprite_name,
            Rotation.R0,
            new_x,
            new_y,
            self.zoom,
            self.frame if frame == -1 else frame
        )

    def update_pacman_render(self):
        direction = self.game_state.pacman.direction
        pos_y, pos_x = self.game_state.pacman.position
        frame = -1

        if direction == Direction.NONE and self.previous_direction == Direction.NONE:
            sprite_name = self.pacman_sprites_name.normal.sprites_for_direction[Direction.UP]
            frame = 2
        elif direction == Direction.NONE and self.previous_direction != Direction.NONE:
            sprite_name = self.pacman_sprites_name.normal.sprites_for_direction[self.previous_direction]
        else:
            self.previous_direction = direction
            sprite_name = self.pacman_sprites_name.normal.sprites_for_direction[direction]
        self.update_sprite(sprite_name, pos_x, pos_y, frame)

    def update_ghosts_render(self):
        for ghost in self.game_state.ghosts:
            direction = ghost.direction
            pos_y, pos_x = ghost.position

            if ghost.state == GhostState.HUNTER:
                if direction == Direction.NONE:
                    sprite_name = self.ghosts_sprites_name[ghost.name].normal.sprites_for_direction[Direction.UP]
                else:
                    sprite_name = self.ghosts_sprites_name[ghost.name].normal.sprites_for_direction[direction]

            elif ghost.state == GhostState.HUNTED:
                if self.game_state.time_hunt_ghosts <= 3.0 and self.frame % 4 <= 1:
                    sprite_name = self.ghosts_sprites_name[ghost.name].fear_white
                else:
                    sprite_name = self.ghosts_sprites_name[ghost.name].fear_blue

            elif ghost.state == GhostState.EATEN:
                if direction == Direction.NONE:
                    sprite_name = self.ghosts_sprites_name[ghost.name].death.sprites_for_direction[Direction.UP]
                else:
                    sprite_name = self.ghosts_sprites_name[ghost.name].death.sprites_for_direction[direction]

            self.update_sprite(sprite_name, pos_x, pos_y)

    def update_pacgums_render(self):
        for y in range(len(self.game_state.grid.cells)):
            for x in range(len(self.game_state.grid.cells[y])):
                if self.game_state.grid.cells[y][x].content == CellContents.PACGUM:
                    sprite_name = self.pacgums_sprites_name.pacgum
                elif self.game_state.grid.cells[y][x].content == CellContents.SUPER_PACGUM:
                    sprite_name = self.pacgums_sprites_name.super_pacgum
                else:
                    continue
                self.update_sprite(sprite_name, x, y)

    def update_animation(self, dt):
        self.frame += 1

    def update_position(self):
        self.buffer_view.fill(0)

        if self.game_state.status == GameStatus.PLAYING:
            self.update_pacgums_render()
            self.update_ghosts_render()
            self.update_pacman_render()


class Render(window.Window):
    def __init__(self):

        # Spritesheets
        self.maze_spritesheet = SpriteSheetManager(
            "assets/maze_spritesheet_config.json",
            "assets/maze_spritesheet.png",
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

        self.curr_level = -1

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # Config
        game_config = ConfigParser().load_config("config.json", GameConfig)

        self.game_state = GameState(game_config)
        self.game_state.switch_cheat_mode()
        self.game_state.switch_speed_pacman()

        # Buffer
        initial_maze_width = game_config.width * \
            self.maze_spritesheet.spritesheet_config.tile_size * \
            3

        initial_maze_height = game_config.height * \
            self.maze_spritesheet.spritesheet_config.tile_size * \
            3

        self.zoom = max(1, min(
                screen.width // initial_maze_width,
                screen.height // initial_maze_height
            ))

        self.maze_spritesheet.preloading_sprites(
            [Rotation.R0, Rotation.R90, Rotation.R180, Rotation.R270],
            self.zoom)
        self.entities_spritesheet.preloading_sprites(
            [Rotation.R0],
            self.zoom
        )

        self.maze_width = initial_maze_width * self.zoom
        self.maze_height = initial_maze_height * self.zoom

        self.maze_pitch = self.maze_width * self.maze_spritesheet.bytes_number_per_pixel
        self.entities_pitch = self.maze_width * self.entities_spritesheet.bytes_number_per_pixel

        self.maze_buffer, self.maze_buffer_view = self._create_buffer(self.maze_width, self.maze_height, self.maze_pitch, self.maze_spritesheet.bytes_number_per_pixel)
        self.entities_buffer, self.entities_buffer_view = self._create_buffer(self.maze_width, self.maze_height, self.entities_pitch, self.entities_spritesheet.bytes_number_per_pixel)

        self.wall_renderer = WallRenderer(self.maze_spritesheet)

        self.entities_renderer = EntitiesRenderer(
            self.game_state, 
            self.entities_buffer_view, 
            self.entities_pitch,
            self.entities_spritesheet,
            self.zoom
        )

        self.direction_input = {
            key.W: Direction.UP,
            key.D: Direction.RIGHT,
            key.S: Direction.DOWN,
            key.A: Direction.LEFT
        }
        
        clock.schedule_interval(self.entities_renderer.update_animation, 0.11)
        clock.schedule_interval(self.game_state.update, 0.01)

    @staticmethod
    def _create_buffer(width, height, pitch, bytes_number_per_pixel):
        buffer = bytearray(int(pitch * height))
        buffer_view = frombuffer(buffer, dtype=uint8).reshape(height, width, bytes_number_per_pixel)
        return buffer, buffer_view

    def on_key_press(self, symbol, modifiers):
        direction = self.direction_input.get(symbol)
        if direction is not None:
            self.game_state.wanted_direction = direction

    def on_draw(self):
        self.clear()
        if self.curr_level != self.game_state.level:
            self.wall_renderer.create_maze_render(self.game_state.grid.cells, self.maze_buffer_view, self.zoom)
            self.curr_level = self.game_state.level

        maze_img = image.ImageData(
            self.maze_width, self.maze_height,
            "RGB",
            bytes(self.maze_buffer),
            pitch=-self.maze_pitch
        )

        self.entities_renderer.update_position()

        entities_img = image.ImageData(self.maze_width, self.maze_height, "RGBA", bytes(self.entities_buffer), pitch=-self.entities_pitch)

        maze_img.blit(100, self.height - 50 - self.maze_height)
        entities_img.blit(100, self.height - 50 - self.maze_height)

render = Render()
# # test to run pipeline

app.run()
