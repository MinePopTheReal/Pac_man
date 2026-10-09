from pyglet import window, app, sprite, image, clock
from src.maze_renderer.wall_renderer import WallRenderer
from src.maze.loader import generate_maze
from src.game_state.game_state import GameState, Direction
from src.parsing.parse_config import ConfigParser
from src.parsing.models import GameConfig, Spritesheet
from src.utils.sprite_sheet_manager import SpriteSheetManager
from pyglet.window import key
from pyglet import gl

















window = window.Window(800, 600, "PacMan")

game_config = ConfigParser().load_config("config.json", GameConfig)
game_state = GameState(game_config)

maze = generate_maze(20, 20, 0, 50)
wall_renderer = WallRenderer(maze.cells)

maze_img = wall_renderer.create_maze_render()

width, height = wall_renderer.maze_width * 3 * 8, wall_renderer.maze_height * 3 * 8

img = image.ImageData(
    width, height,
    "RGB",
    bytes(maze_img),
    pitch=-width * 3
)

# sprite = sprite.Sprite(maze_img)
# buffer = bytearray(
#     wall_renderer.maze_width
#     * wall_renderer.spritesheet.spritesheet_config.tile_size
#     * 4
#     * wall_renderer.buffer_pitch
#     )

# spritesheet = ConfigParser().load_config("assets/entities_spritesheet_config.json", Spritesheet)

spritesheet = SpriteSheetManager(
    "assets/entities_spritesheet_config.json",
    "assets/entities_spritesheet.png",
    "RGBA"
)
width, height = wall_renderer.maze_width * 3 * 8, wall_renderer.maze_height * 3 * 8
bpp = spritesheet.bytes_number_per_pixel
w_pitch = width * bpp
buffer = bytearray(w_pitch * height)
frame = 0

def advance_animation(dt):
    global frame
    frame = (frame + 1) % 3

def update_pacman_render():
    # ne modifie plus frame : elle se contente de le lire
    sprite_per_direction = {
        Direction.NONE.name: "pacman_top",
        Direction.UP.name: "pacman_top",
        Direction.LEFT.name: "pacman_left",
        Direction.RIGHT.name: "pacman_right",
        Direction.DOWN.name: "pacman_bottom"
        }
    
    tile_name = sprite_per_direction[game_state.pacman.direction.name]
    return spritesheet.take_tile(tile_name, frame)

clock.schedule_interval(advance_animation, 0.11)
clock.schedule_interval(game_state.update, 0.1)
# def update_pacman_render():
#     global frame



#     tile_name = sprite_per_direction[game_state.pacman.direction.name]
#     frame = (frame + 1) % 3
#     return spritesheet.take_tile(tile_name, frame)



# clock.schedule_interval(game_state.update, 10)

# @window.event
# def on_draw():
#     window.clear()

#     pacman_sprite = update_pacman_render()
#     spritesheet.copy_tile_into_buffer(buffer, w_pitch, pacman_sprite, 3, 3)

#     img_pacman = image.ImageData(
#         width, height,
#         "RGBA",
#         bytes(buffer),
#         pitch=-w_pitch
#     )
    
#     img.blit(100, window.height - 50 - height)
#     img_pacman.blit(100, window.height - 50 - height)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

direction_input = {
    key.W: Direction.UP,
    key.D: Direction.RIGHT,
    key.S: Direction.DOWN,
    key.A: Direction.LEFT
}

@window.event
def on_key_press(symbol, modifiers):
    direction = direction_input.get(symbol)
    if direction is not None:
        print(direction)
        game_state.wanted_direction = direction

from time import sleep
@window.event
def on_draw():
    window.clear()

    img.blit(0, 0)

    x, y = game_state.pacman.position

    tile = update_pacman_render()
    pacman_img = image.ImageData(16, 16, "RGBA", bytes(tile), pitch=-16 * 4)
    print((int(y) + 8) * 8 + 3, (int(x) + 8) * 8 + 3)
    sleep(0.2)
    pacman_img.blit((int(y) + 8) * 8 + 3, (int(x) + 8) * 8 + 3)

app.run()
