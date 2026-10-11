from enum import IntEnum
from pyglet import image

from src.parsing.parse_config import ConfigParser
from src.parsing.models import Spritesheet
from src.maze.loader import generate_maze
from src.maze.grid import Direction
from src.maze.cell import Cell


class Rotation(IntEnum):
    R0 = 0
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

        self.bytes_number_per_pixel: int = 3

        self.spritesheet_config: Spritesheet = self._load_maze_sprite_config()
        self.spritesheet_data: bytes = self._load_sprite_data()

        self.maze_height = len(self.maze)
        self.maze_width = len(self.maze[0])

        self.buffer_pitch: int = self.maze_width * self.spritesheet_config.tile_size * 3 * self.bytes_number_per_pixel
        self.buffer = bytearray(self.maze_height * self.spritesheet_config.tile_size * 3 * self.buffer_pitch)


    def _load_maze_sprite_config(self):
        parser = ConfigParser()
        spritesheet = parser.load_config(self.paths["config"], Spritesheet)
        return spritesheet

    def _load_sprite_data(self):
        png_spritesheet = image.load("assets/maze_spritesheet.png")
        raw_spritesheet = png_spritesheet.get_image_data()

        self.pitch = -raw_spritesheet.width * self.bytes_number_per_pixel

        image_data = raw_spritesheet.get_data("RGB", self.pitch)
        return image_data


    def create_maze_render(self):
        for maze_y in range(self.maze_height):
            for maze_x in range(self.maze_width):
                self._create_tiles_for_one_coord(maze_x, maze_y)

    def is_full_cell(self, cell: Cell):
        if (
            cell.there_is_wall(Direction.UP)
            and cell.there_is_wall(Direction.DOWN)
            and cell.there_is_wall(Direction.LEFT)
            and cell.there_is_wall(Direction.RIGHT)
        ):
            return True
        return False

    def _is_on_the_edge(self, sub_x: int, sub_y:int, x: int, y: int):
        if (
            y == 0 and sub_y == 0
            or x == self.maze_width - 1 and sub_x == 2
            or y == self.maze_height - 1 and sub_y == 2
            or x == 0  and sub_x == 0
        ):
            return True
        return False


    # NEIGHBORS = {
    #     "TL": ("up",   "left",  "down", "right"),
    #     "TR": ("up",   "right", "down", "left"),
    #     "BL": ("down", "left",  "up",   "right"),
    #     "BR": ("down", "right", "up",   "left"),
    # }





    # def _has_wall(self, x: int, y: int, direction: Direction) -> bool:
    #     if 0 <= x < self.maze_width and 0 <= y < self.maze_height:
    #         return self.maze[y][x].there_is_wall(direction)
    #     return False

    # def _vertex_edges(self, vx: int, vy: int) -> dict[str, bool]:
    #     w = self._has_wall
    #     return {
    #         "up":    w(vx - 1, vy - 1, Direction.RIGHT) or w(vx, vy - 1, Direction.LEFT),
    #         "down":  w(vx - 1, vy, Direction.RIGHT) or w(vx, vy, Direction.LEFT),
    #         "left":  w(vx - 1, vy - 1, Direction.DOWN) or w(vx - 1, vy, Direction.UP),
    #         "right": w(vx, vy - 1, Direction.DOWN) or w(vx, vy, Direction.UP)
    #     }

    # def _inner_corner_tile(self, quadrant: str, edges: dict[str, bool]):
    #     vertical, horizontal, opp_vertical, opp_horizontal = self.NEIGHBORS[quadrant]
    #     if edges[vertical] and edges[horizontal]:
    #         return "corner", self.ARC_INSIDE[quadrant]
    #     if edges[vertical]:
    #         return "line", Rotation.R90 if quadrant in ("TL", "BL") else Rotation.R270
    #     if edges[horizontal]:
    #         return "line", Rotation.R180 if quadrant in ("TL", "TR") else Rotation.R0
    #     if edges[opp_vertical] or edges[opp_horizontal]:
    #         return "corner", self.ARC_AROUND[quadrant]
    #     return "black_tile", Rotation.R0

    # def _border_corner_tile(self, vx: int, vy: int, quadrant: str, edges: dict[str, bool]):
    #     top, bottom = vy == 0, vy == self.maze_height
    #     left, right = vx == 0, vx == self.maze_width
    #     if (top or bottom) and (left or right):
    #         return "double_corner", self.ARC_INSIDE[quadrant]
    #     if top:
    #         side, rot = "down", Rotation.R0
    #         inward = {"BL": "line_and_corner_right", "BR": "line_and_corner_left"}
    #     elif bottom:
    #         side, rot = "up", Rotation.R180
    #         inward = {"TL": "line_and_corner_left", "TR": "line_and_corner_right"}
    #     elif left:
    #         side, rot = "right", Rotation.R270
    #         inward = {"TR": "line_and_corner_left", "BR": "line_and_corner_right"}
    #     else:
    #         side, rot = "left", Rotation.R90
    #         inward = {"TL": "line_and_corner_right", "BL": "line_and_corner_left"}
    #     if edges[side]:
    #         return inward[quadrant], rot
    #     return "double_line", rot

    # def _choose_corner_tile(self, x: int, y: int, corner: tuple[int, int]):
    #     dx, dy, quadrant = self.CORNER_TILES[corner]
    #     vx, vy = x + dx, y + dy
    #     edges = self._vertex_edges(vx, vy)
    #     if vx in (0, self.maze_width) or vy in (0, self.maze_height):
    #         return self._border_corner_tile(vx, vy, quadrant, edges)
    #     return self._inner_corner_tile(quadrant, edges)

    NEIGHBORS = {
        "TL": ("up",   "left",  "down", "right"),
        "TR": ("up",   "right", "down", "left"),
        "BL": ("down", "left",  "up",   "right"),
        "BR": ("down", "right", "up",   "left")
    }

    ARC_INSIDE = {
        "TL": Rotation.R0,   
        "TR": Rotation.R90,
        "BR": Rotation.R180, 
        "BL": Rotation.R270
    }

    ARC_AROUND = {
        "TL": Rotation.R180,
        "TR": Rotation.R270,
        "BL": Rotation.R90,  
        "BR": Rotation.R0
    }

    CORNER_TILES = {
        (0, 0): ("TL", 0, 0),
        (2, 0): ("TR", 1, 0),
        (0, 2): ("BL", 0, 1),
        (2, 2): ("BR", 1, 1)
    }

    def has_wall(self, x: int, y: int, direction: Direction) -> bool:
        if 0 <= x < self.maze_width and 0 <= y < self.maze_height:
            return self.maze[y][x].there_is_wall(direction)
        return False

    def get_wall_by_neighbors(self, x, y):
        w = self.has_wall

        return {
            "up": w(x, y - 1, Direction.LEFT),
            "left": w(x - 1, y, Direction.UP),
            "down": w(x, y, Direction.LEFT),
            "right": w(x, y, Direction.UP)
        }

    def choose_border_corner(self, x, y, position, walls):
        return ("black_tile", Rotation.R0)

    def choose_normal_corner(self, x, y, position, walls):
        vertical, horizontal, opposite_vertical, opposite_horizontal = self.NEIGHBORS[position]

        if walls[vertical] and walls[horizontal]:
            return "corner", self.ARC_AROUND[position]

        if walls[vertical]:
            return "line",  Rotation.R270 if position in ("TL", "BL") else Rotation.R90

        if walls[horizontal]:
            return "line",  Rotation.R0 if position in ("TL", "TR") else Rotation.R180

        if walls[opposite_vertical] or walls[opposite_horizontal]:
            return "corner", self.ARC_INSIDE[position]

        return ("black_tile", Rotation.R0)

    def choose_corner_tile(self, x, y, corner_x, corner_y):
        position, dx, dy = self.CORNER_TILES[(corner_x, corner_y)]

        vx, vy = x + dx, y + dy
        walls = self.get_wall_by_neighbors(vx, vy)
        if vx in (0, self.maze_width) or vy in (0, self.maze_height):
            return self.choose_border_corner(x, y, position, walls)
        return self.choose_normal_corner(x, y, position, walls)

    def _choose_tiles(self, x: int, y: int) -> list[list[tuple[str, Rotation]]]:
        side_coords = {
            (1, 0): (Direction.UP, Rotation.R0),
            (0, 1): (Direction.LEFT, Rotation.R270),
            (2, 1): (Direction.RIGHT, Rotation.R90),
            (1, 2): (Direction.DOWN, Rotation.R180)
        }
        tiles = [[("black_tile", Rotation.R0) for _ in range(3)] for _ in range(3)]
        cell = self.maze[y][x]

        for (sx, sy), (direction, rotation) in side_coords.items():
            if cell.there_is_wall(direction):
                name = "double_line" if self._is_on_the_edge(sx, sy, x, y) else "line"
                tiles[sy][sx] = (name, rotation)

        for corner_x, corner_y in self.CORNER_TILES:
            tile = self.choose_corner_tile(x, y, corner_x, corner_y)
            tiles[corner_y][corner_x] = tile
        return tiles
        # for corner_x, corner_y in self.CORNER_TILES:
        #     tiles[corner_y][corner_x] = self._choose_corner_tile(x, y, (corner_x, corner_y))
        # return tiles

    def _create_tiles_for_one_coord(self, maze_x: int, maze_y: int):
        tile_size = self.spritesheet_config.tile_size

        tiles = self._choose_tiles(maze_x, maze_y)

        for sub_y in [maze_y * 3, maze_y * 3 + 1, maze_y * 3 + 2]:
            for sub_x in [maze_x * 3, maze_x * 3 + 1, maze_x * 3 + 2]:
                tile_name, rotation = tiles[sub_y % 3][sub_x % 3]
                tile = self._take_tile(tile_name)
                tile = self._rotate_tile(tile, rotation)

                self._copy_tile_into_buffer(
                    tile,
                    sub_x * tile_size,
                    sub_y * tile_size,
                )

    def R90(self, x: int, y: int):
        return (self.spritesheet_config.tile_size - 1 - y, x)


    def R180(self, x: int, y: int):
        return (self.spritesheet_config.tile_size - 1 - x, self.spritesheet_config.tile_size - 1 - y)


    def R270(self, x: int, y: int):
        return (y, self.spritesheet_config.tile_size - 1 - x)


    def _rotate_tile(self, bytes_tile: bytearray, deg: Rotation): # util func for animation
        temp_tile: bytearray = bytearray(self.spritesheet_config.tile_size * 3 * self.spritesheet_config.tile_size)

        if deg == Rotation.R0:
            return bytes_tile

        formula = {
            Rotation.R90: self.R90,
            Rotation.R180: self.R180,
            Rotation.R270: self.R270
        }

        for y_px in range (self.spritesheet_config.tile_size):
            for x_px in range (self.spritesheet_config.tile_size):
                pitch = y_px * self.spritesheet_config.tile_size * self.bytes_number_per_pixel
                pixel_data = bytes_tile[x_px * self.bytes_number_per_pixel + pitch:x_px * self.bytes_number_per_pixel + pitch + self.bytes_number_per_pixel]

                new_x, new_y = formula[deg](x_px, y_px)
                new_pitch = new_y * self.spritesheet_config.tile_size * self.bytes_number_per_pixel
                temp_tile[new_x * self.bytes_number_per_pixel + new_pitch:new_x * self.bytes_number_per_pixel + new_pitch + self.bytes_number_per_pixel] = pixel_data
        return temp_tile

    def _take_tile(self, tile_name: str): # util func for animation
        temp_tile: bytearray = bytearray()

        tile_coord = self.spritesheet_config.tiles[tile_name][0]

        for y_px in range(self.spritesheet_config.tile_size):
            tile_x = ((tile_coord.y + y_px) * abs(self.pitch) + tile_coord.x * self.bytes_number_per_pixel)
            temp_tile += bytearray(self.spritesheet_data[tile_x:tile_x + self.spritesheet_config.tile_size * self.bytes_number_per_pixel])
        return temp_tile

    def _copy_tile_into_buffer(self, tile: bytearray, x: int, y: int):
        for y_px in range(self.spritesheet_config.tile_size):
            tile_pitch = y_px * self.spritesheet_config.tile_size * self.bytes_number_per_pixel

            buffer_x = ((y + y_px) * abs(self.buffer_pitch) + x * self.bytes_number_per_pixel)

            self.buffer[buffer_x:buffer_x + self.spritesheet_config.tile_size * self.bytes_number_per_pixel] = tile[tile_pitch:tile_pitch + self.spritesheet_config.tile_size * self.bytes_number_per_pixel]

    def test_display(self, array: bytearray | None = None):
        from math import sqrt
        from PIL import Image

        size = int(sqrt(len(array or self.buffer) / self.bytes_number_per_pixel))
        img = Image.frombytes("RGB", (size, size), array or self.buffer)
        img.save("debug/debug_render_1.png")

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
    maze = generate_maze(20, 20, 4)
    renderer = MazeRenderer(maze.grid)

    renderer.create_maze_render()

    renderer.test_display()
