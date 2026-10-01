from enum import IntEnum
from pyglet import image

from src.parsing.parse_config import ConfigParser
from src.parsing.models import Spritesheet
from src.maze.loader import generate_maze
from src.maze.cell import Cell



class Rotation(IntEnum):
    R90 = 90
    R180 = 180
    R270 = 270


class MazeRenderer:
    def __init__(self, maze: list[list[Cell]]):
        
        self.paths: dict[str, str] = {
            "spritesheet": "assets/maze_spritesheet.png",
            "config": "assets/maze_spritesheet_config.json"
            }

        self.maze: list[list[Cell]] = maze

        self.spritesheet_config: Spritesheet = self._load_maze_sprite_config()
        self.spritesheet_data: bytes = self._load_sprite_data()

        self.maze_height = len(self.maze)
        self.maze_width = len(self.maze[0])

        self.buffer_pitch: int = self.maze_width * self.spritesheet_config.tile_size * 3 * 4
        self.buffer = bytearray(self.maze_height * self.spritesheet_config.tile_size * 3 * self.buffer_pitch)

    def _load_maze_sprite_config(self):
        parser = ConfigParser()
        spritesheet = parser.load_config(self.paths["config"], Spritesheet)
        return spritesheet

    def _load_sprite_data(self):
        png_spritesheet = image.load("assets/maze_spritesheet.png")
        raw_spritesheet = png_spritesheet.get_image_data()

        self.pitch = raw_spritesheet.pitch

        image_data = raw_spritesheet.get_data("RGBA", self.pitch)
        return image_data

    # def _create_empty_buffer(self, tile_size, maze_height, maze_width):
    #     # self.buffer = np.zeros(
    #     #     (
    #     #         tile_size * maze_height * 3,
    #     #         tile_size * maze_width * 3,
    #     #         3
    #     #     ),
    #     #     dtype=np.uint8
    #     # )


    def create_maze_render(self):


        # self._create_empty_buffer(
        #     self.spritesheet_config.tile_size, 
        #     maze_height, 
        #     maze_width
        # )

        for maze_y in range(self.maze_height):
            for maze_x in range(self.maze_width):
                self._create_tiles_for_one_coord(maze_x, maze_y)

    def _choose_tile(cell):
        ...

    def _create_tiles_for_one_coord(self, maze_x: int, maze_y: int):
        cell = self.maze[maze_y][maze_x]
        tile_size = self.spritesheet_config.tile_size

        for sub_y in [maze_y * 3, maze_y * 3 + 1, maze_y * 3 + 2]:
            for sub_x in [maze_x * 3, maze_x * 3 + 1, maze_x * 3 + 2]:
                tile_1 = self._take_tile("corner")
                self._copy_tile_into_buffer(
                    tile_1,
                    sub_x * tile_size,   # conversion unité de tuile -> pixels
                    sub_y * tile_size,
                )

    def R90(self, x: int, y: int):
        return (self.spritesheet_config.tile_size - 1 - y, x)


    def R180(self, x: int, y: int):
        return (self.spritesheet_config.tile_size - 1 - x, self.spritesheet_config.tile_size - 1 - y)


    def R270(self, x: int, y: int):
        return (y, self.spritesheet_config.tile_size - 1 - x)


    def _rotate_tile(self, bytes_tile: bytearray, deg: Rotation): # util func for animation
        temp_tile: bytearray = bytearray(self.spritesheet_config.tile_size * 4 * self.spritesheet_config.tile_size)
        
        formula = {
            Rotation.R90: self.R90,
            Rotation.R180: self.R180,
            Rotation.R270: self.R270
        }

        for y_px in range (self.spritesheet_config.tile_size):
            for x_px in range (self.spritesheet_config.tile_size):
                pitch = y_px * self.spritesheet_config.tile_size * 4
                pixel_data = bytes_tile[x_px * 4 + pitch:x_px * 4 + pitch + 4]

                new_x, new_y = formula[deg](x_px, y_px)
                new_pitch = new_y * self.spritesheet_config.tile_size * 4
                temp_tile[new_x * 4 + new_pitch:new_x * 4 + new_pitch + 4] = pixel_data
        return temp_tile
        # for nb_rotate in range(deg % 90):

    def _take_tile(self, tile_name: str): # util func for animation
        temp_tile: bytearray = bytearray()

        tile_coord = self.spritesheet_config.tiles[tile_name][0]

        for y_px in range(self.spritesheet_config.tile_size):
            tile_x = ((tile_coord.y + y_px) * abs(self.pitch) + tile_coord.x * 4)
            temp_tile += bytearray(self.spritesheet_data[tile_x:tile_x + self.spritesheet_config.tile_size * 4])
        return temp_tile

    def _copy_tile_into_buffer(self, tile: bytearray, x: int, y: int):
        for y_px in range(self.spritesheet_config.tile_size):
            tile_pitch = y_px * self.spritesheet_config.tile_size * 4

            buffer_x = ((y + y_px) * abs(self.buffer_pitch) + x * 4)

            self.buffer[buffer_x:buffer_x + self.spritesheet_config.tile_size * 4] = tile[tile_pitch:tile_pitch + self.spritesheet_config.tile_size * 4]

    def test_display(self, array: bytearray | None = None):
        from math import sqrt
        from PIL import Image

        print(array)
        size = int(sqrt(len(array or self.buffer) / 4))
        print(size)
        print(len(array))
        img = Image.frombytes("RGBA", (size, size), array or self.buffer)
        img = img.resize((size * 20, size * 20), Image.NEAREST)
        img.save("debug/debug_render_1.png")
        img.show()

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
    renderer = MazeRenderer(maze.grid)

    # renderer.create_maze_render()
    tile_1 = renderer._take_tile("corner")
    tile_2 = renderer._rotate_tile(tile_1, Rotation.R90)

    renderer.test_display(tile_2)
