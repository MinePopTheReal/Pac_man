from pyglet import window, app, sprite, image, clock, display
from src.maze_renderer.wall_renderer import WallRenderer
from src.maze.loader import generate_maze
from src.game_state.game_state import GameState, Direction, GameStatus
from src.parsing.parse_config import ConfigParser
from src.parsing.models import GameConfig, Spritesheet
from src.utils.sprite_sheet_manager import SpriteSheetManager
from pyglet.window import key
from pyglet import gl
from math import floor
from src.entity.ghost import GhostState
from src.maze.grid import CellContents


from dataclasses import dataclass

@dataclass
class CharactersSprites():
    sprites_for_direction: dict[Direction, list[bytearray]]

@dataclass
class PacManSprites():
    normal: CharactersSprites
    death: list[bytearray]

@dataclass
class GhostsSprites():
    normal: CharactersSprites
    death: CharactersSprites
    fear_blue: list[bytearray]
    fear_white: list[bytearray]

@dataclass
class PacGumSprites():
    super_pacgum: bytearray
    pacgum: bytearray
    

class EntitiesRenderer:
    def __init__(self, game_state: GameState, buffer: bytearray, buffer_pitch: int, spritesheet: SpriteSheetManager, zoom: int):

        self.game_state = game_state

        self.spritesheet = spritesheet
        
        self.zoom = zoom

        self.pacman_sprites = self.load_pacman_sprites()
        self.pacgums_sprites = self.load_pacgums_sprites()
        self.ghosts_sprites = self.load_ghosts_sprites()

        self.buffer: bytearray = buffer
        self.buffer_pitch: int = buffer_pitch

        self.previous_direction: Direction = Direction.NONE

        self.frame = 0

    def load_pacman_sprites(self):
        return PacManSprites(
            normal=CharactersSprites({
                Direction.UP: self.spritesheet.take_tiles("pacman_top"),
                Direction.RIGHT: self.spritesheet.take_tiles("pacman_right"),
                Direction.DOWN: self.spritesheet.take_tiles("pacman_bottom"),
                Direction.LEFT: self.spritesheet.take_tiles("pacman_left")
            }),
            death=self.spritesheet.take_tiles("pacman_death")
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
                    Direction.UP: self.spritesheet.take_tiles(sprite_name[0]),
                    Direction.RIGHT: self.spritesheet.take_tiles(sprite_name[1]),
                    Direction.DOWN: self.spritesheet.take_tiles(sprite_name[2]),
                    Direction.LEFT: self.spritesheet.take_tiles(sprite_name[3])
                }),
                death=CharactersSprites({
                    Direction.UP: self.spritesheet.take_tiles("ghosts_eyes_top"),
                    Direction.RIGHT: self.spritesheet.take_tiles("ghosts_eyes_right"),
                    Direction.DOWN: self.spritesheet.take_tiles("ghosts_eyes_bottom"),
                    Direction.LEFT: self.spritesheet.take_tiles("ghosts_eyes_left")
                }),
                fear_blue=self.spritesheet.take_tiles("ghosts_fear_blue"),
                fear_white=self.spritesheet.take_tiles("ghosts_fear_white") 
            )
        return loaded_sprites

    def load_pacgums_sprites(self):
        return PacGumSprites(
            super_pacgum=self.spritesheet.take_tiles("super_pacgum")[0],
            pacgum=self.spritesheet.take_tiles("pacgum")[0]
        )

    @staticmethod
    def float_to_pixel(position_x: float, position_y: float, zoom: int):
        return (int(position_x * 8 * 3), int(position_y * 8 * 3))

    def update_pacman_render(self):
        direction = self.game_state.pacman.direction
        pos_y, pos_x = self.game_state.pacman.position

        if direction == Direction.NONE and self.previous_direction == Direction.NONE:
            sprite = self.pacman_sprites.normal.sprites_for_direction[Direction.UP][2]
        elif direction == Direction.NONE and self.previous_direction != Direction.NONE:
            sprite = self.pacman_sprites.normal.sprites_for_direction[self.previous_direction][1]
        else:
            self.previous_direction = direction
            sprite = self.pacman_sprites.normal.sprites_for_direction[direction][self.frame % len(self.pacman_sprites.normal.sprites_for_direction[direction])]

        new_position = self.float_to_pixel(pos_x, pos_y, self.zoom)
        self.spritesheet.copy_tile_into_buffer(
            self.buffer,
            self.buffer_pitch,
            sprite,
            new_position[0] + 4,
            new_position[1] + 4,
            self.zoom
        )

    def update_ghosts_render(self):
        for ghost in self.game_state.ghosts:
            self.ghosts_sprites[ghost.name]
            
            direction = ghost.direction
            pos_y, pos_x = ghost.position
            
            if ghost.state == GhostState.HUNTER: 
                if direction == Direction.NONE:
                    sprite = self.ghosts_sprites[ghost.name].normal.sprites_for_direction[Direction.UP][self.frame % len(self.ghosts_sprites[ghost.name].normal.sprites_for_direction[Direction.UP])]
                else:
                    sprite = self.ghosts_sprites[ghost.name].normal.sprites_for_direction[direction][self.frame % len(self.ghosts_sprites[ghost.name].normal.sprites_for_direction[direction])]
                    
            elif ghost.state == GhostState.HUNTED:
                if self.game_state.time_hunt_ghosts <= 3.0 and self.frame % 4 <= 1:
                    sprites = self.ghosts_sprites[ghost.name].fear_white
                else:
                    sprites = self.ghosts_sprites[ghost.name].fear_blue
                    
                if direction == Direction.NONE:
                    sprite = sprites[0]
                else:
                    sprite = sprites[self.frame % len(sprites)]

            elif ghost.state == GhostState.EATEN: 
                if direction == Direction.NONE:
                    sprite = self.ghosts_sprites[ghost.name].death.sprites_for_direction[Direction.UP][self.frame % len(self.ghosts_sprites[ghost.name].death.sprites_for_direction[Direction.UP])]
                else:
                    sprite = self.ghosts_sprites[ghost.name].death.sprites_for_direction[direction][self.frame % len(self.ghosts_sprites[ghost.name].death.sprites_for_direction[direction])]
            
            new_position = self.float_to_pixel(pos_x, pos_y, self.zoom)
            self.spritesheet.copy_tile_into_buffer(
                self.buffer,
                self.buffer_pitch,
                sprite,
                new_position[0] + 4,
                new_position[1] + 4,
                self.zoom
            )
            

    def update_pacgums_render(self):
        for y in range(len(self.game_state.grid.cells)):
            for x in range(len(self.game_state.grid.cells[y])):
                if self.game_state.grid.cells[y][x].content == CellContents.PACGUM:
                    sprite = self.pacgums_sprites.pacgum
                elif self.game_state.grid.cells[y][x].content == CellContents.SUPER_PACGUM:
                    sprite = self.pacgums_sprites.super_pacgum
                else:
                    continue
                new_position = self.float_to_pixel(x, y, self.zoom)
                self.spritesheet.copy_tile_into_buffer(
                    self.buffer,
                    self.buffer_pitch,
                    sprite,
                    new_position[0] + 4,
                    new_position[1] + 4,
                    self.zoom
                )
            

    def update_animation(self, dt):
        self.frame += 1
        # self.update_pacman_render()

    def update_position(self):
        self.buffer[:] = b'\x00' * len(self.buffer)
        # if not in pause
        if self.game_state.status == GameStatus.PLAYING:
            self.update_pacgums_render()
            self.update_ghosts_render()
            self.update_pacman_render()


class Render(window.Window):
    def __init__(self):
        # Display config
        display_data = display.get_display()
        screen = display_data.get_default_screen()

        super().__init__(width=screen.width, height=screen.height, caption="Pac-Man")

        # self.window = window.Window(screen.width, screen.height, "PacMan")

        self.curr_level = -1

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        

        # Spritesheets
        self.maze_spritesheet = SpriteSheetManager(
            "assets/maze_spritesheet_config.json",
            "assets/maze_spritesheet.png",
            "RGB"
        )
        self.entities_spritesheet = SpriteSheetManager(
            "assets/entities_spritesheet_config.json",
            "assets/entities_spritesheet.png",
            "RGBA"
        )

        # Config
        game_config = ConfigParser().load_config("config.json", GameConfig)

        self.game_state = GameState(game_config)

        # Buffer
        initial_maze_width = game_config.width * \
            self.maze_spritesheet.spritesheet_config.tile_size * \
            3

        initial_maze_height = game_config.height * \
            self.maze_spritesheet.spritesheet_config.tile_size * \
            3

        print(screen.width, screen.height)

        self.zoom_multiplier = max(1, min(
                screen.width // initial_maze_width,
                screen.height // initial_maze_height
            ))

        self.maze_width = initial_maze_width * self.zoom_multiplier
        self.maze_height = initial_maze_height * self.zoom_multiplier

        self.maze_pitch = self.maze_width * self.maze_spritesheet.bytes_number_per_pixel
        self.entities_pitch = self.maze_width * self.entities_spritesheet.bytes_number_per_pixel

        self.maze_buffer = self._create_buffer(self.maze_pitch, self.maze_height)
        self.entities_buffer = self._create_buffer(self.entities_pitch, self.maze_height)

        self.wall_renderer = WallRenderer(self.maze_spritesheet)

        self.entities_renderer = EntitiesRenderer(
            self.game_state, 
            self.entities_buffer, 
            self.entities_pitch,
            self.entities_spritesheet,
            self.zoom_multiplier
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
    def _create_buffer(width, height):
        return bytearray(width * height)

    def on_key_press(self, symbol, modifiers):
        direction = self.direction_input.get(symbol)
        if direction is not None:
            self.game_state.wanted_direction = direction

    def on_draw(self):
        if self.curr_level != self.game_state.level:
            self.wall_renderer.create_maze_render(self.game_state.grid.cells, self.maze_buffer, self.maze_pitch, self.zoom_multiplier)
            self.curr_level = self.game_state.level
            # print(self.maze_buffer)


        maze_img = image.ImageData(
            self.maze_width, self.maze_height,
            "RGB",
            bytes(self.maze_buffer),
            pitch=-self.maze_pitch
        )

        self.clear()
        self.entities_renderer.update_position()
    
        entities_img = image.ImageData(self.maze_width, self.maze_height, "RGBA", bytes(self.entities_buffer), pitch=-self.entities_pitch)
    
        maze_img.blit(100, self.height - 50 - self.maze_height)
        entities_img.blit(100, self.height - 50 - self.maze_height)

render = Render()
# # test to run pipeline

app.run()
