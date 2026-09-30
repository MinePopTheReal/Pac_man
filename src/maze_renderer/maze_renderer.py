from pyglet import image
import numpy as np

from src.parsing.parse_config import ConfigParser
from src.parsing.models import Spritesheet
from src.maze.loader import generate_maze
from src.maze.cell import Cell


class MazeRenderer:
    def __init__(self, maze: list[list[Cell]]):
        
        self.paths: dict[str, str] = {
            "spritesheet": "assets/maze_spritesheet.png",
            "config": "assets/maze_spritesheet_config.json"
            }

        self.maze: list[list[Cell]] = maze

        self.spritesheet_config: Spritesheet = self._load_maze_sprite_config()
        self.spritesheet_data: bytes = self._load_sprite_data()

    def _load_maze_sprite_config(self):
        parser = ConfigParser()
        spritesheet = parser.load_config(self.paths["config"], Spritesheet)
        return spritesheet

    def _load_sprite_data(self):
        png_spritesheet = image.load("assets/maze_spritesheet.png")
        raw_spritesheet = png_spritesheet.get_image_data()

        self.pitch = raw_spritesheet.pitch

        raw_spritesheet.get_data("RGBA", self.pitch)

    def _create_empty_buffer(self, tile_size, maze_height, maze_width):
        self.buffer = np.zeros(
            (
                tile_size * maze_height * 3,
                tile_size * maze_width * 3,
                3
            ),
            dtype=np.uint8
        )

    def create_maze_render(self):
        spritesheet = self._load_maze_sprite()

        maze_height = len(self.maze), 
        maze_width = len(self.maze[0])

        self._create_empty_buffer(
            spritesheet.tile_size, 
            maze_height, 
            maze_width
        )

        for maze_y in range(maze_height):
            for maze_x in range(maze_width):
                self._create_tiles_for_one_coord(maze_x, maze_y)


    def _create_tiles_for_one_coord(self, maze_x: int, maze_y: int):
        cell = self.maze[maze_y][maze_x]

        for y_tile in [maze_y * 3, maze_y * 3 + 1, maze_y * 3 + 2]:
            for x_tile in [maze_x * 3, maze_x * 3 + 1, maze_x * 3 + 2]:
                self._copy_tile_into_buffer(x_tile, y_tile, "corner", 0, cell)

    def _rotate_tile(bytes_tile: bytearray, deg: int):
        ...

    def _copy_tile_into_buffer(self, x: int, y: int, tile_name: str, cell: Cell):
        temp_tile: bytearray

        x, y = self.spritesheet_config.tiles[tile_name][0]

        for y_px in range(self.spritesheet_config.tile_size):
            temp_tile = self.spritesheet_data[x:x+self.spritesheet_config.tile_size]



# # for test
# class Graphic:
#     def __init__(self) -> None:
#         self.window = pyglet.window.Window()

#         @self.window.event
#         def on_draw() -> None:
#             self.window.clear()

#         @self.window.event
#         def on_key_press(symbol, modifiers):
#             # print(f"Key pressed: {symbol}")
#             pass


# graphic = Graphic()
# pyglet.app.run()


if __name__ == "__main__":
    maze = generate_maze(25, 25, 42)
    # print(maze.grid.get)
    
    # print(parser.tiles)
    
    
    MazeRenderer(maze)