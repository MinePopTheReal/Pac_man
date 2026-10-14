from src.utils.sprite_sheet_manager import Rotation, SpriteSheetManager
from src.maze.grid import Direction
from src.maze.cell import Cell


class WallRenderer:
    """
    Allows you to create an image composed of tiles to render the maze
    """
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
        (0, 0): ("BR", 0, 0),
        (2, 0): ("BL", 1, 0),
        (0, 2): ("TR", 0, 1),
        (2, 2): ("TL", 1, 1)
    }

    def __init__(self, spritesheet: SpriteSheetManager):
        # self.maze: list[list[Cell]] = maze
        # self.maze_height = len(self.maze)
        # self.maze_width = len(self.maze[0])

        self.spritesheet = spritesheet

    def is_full_cell(self, cell: Cell) -> bool:
        """Checks whether a cell has 4 walls

        Args:
            cell (Cell): Check the cells

        Returns:
            bool: True if the cell have 4 walls else False
        """
        if (
            cell.there_is_wall(Direction.UP)
            and cell.there_is_wall(Direction.DOWN)
            and cell.there_is_wall(Direction.LEFT)
            and cell.there_is_wall(Direction.RIGHT)
        ):
            return True
        return False

    def _is_on_the_edge(self, sub_x: int, sub_y: int, x: int, y: int) -> bool:
        """checks whether a tile is located at the edge of the maze

        Args:
            sub_x (int): coordinate (x) of the tile on the cell

            sub_y (int): coordinate (y) of the tile on the cell

            x (int): coordinates (x) of the cell on which the
            tile is located

            y (int): coordinates (y) of the cell on which the
            tile is located

        Returns:
            bool: True if the tile is at the edge else False
        """
        if (
            y == 0 and sub_y == 0
            or x == self.maze_width - 1 and sub_x == 2
            or y == self.maze_height - 1 and sub_y == 2
            or x == 0 and sub_x == 0
        ):
            return True
        return False

    def has_wall(self, x: int, y: int, direction: Direction) -> bool:
        """Checks whether a cell has a wall in a certain direction

        Args:
            x (int): (x) coordinate of the cell
            y (int): (y) coordinate of the cell
            direction (Direction): the direction to look in

        Returns:
            bool: True if there is a wall else False
        """
        if 0 <= x < self.maze_width and 0 <= y < self.maze_height:
            return self.maze[y][x].there_is_wall(direction)
        return False

    def get_wall_by_neighbors(self, x: int, y: int) -> dict[str, bool]:
        """Allows you to assess, for a given area, which walls whether
        present or not—will affect its condition

        Args:
            x (int): the cell's coordinates (x)
            y (int): the cell's coordinates (y)

        Returns:
            dict[str, bool]:  the directions relative to this tile and whether
            or not a wall is present
        """
        w = self.has_wall

        return {
            "up": w(x, y - 1, Direction.LEFT),
            "left": w(x - 1, y, Direction.UP),
            "down": w(x, y, Direction.LEFT),
            "right": w(x, y, Direction.UP)
        }

    def choose_border_corner(
        self, x: int, y: int, position: str, walls: dict[str, bool]
    ) -> tuple[str, Rotation]:
        """Place the border corners of the cells

        Args:
            x (int): the cell's coordinates (x)
            y (int): the cell's coordinates (y)
            position (str): the position of the corner relative to
            the adjacent cell

            walls (dict[str, bool]): Condition of the adjacent wall affecting
            the condition of the corner of this cell

        Returns:
            tuple[str, Rotation]: Return the cell name and correct the rotation
        """
        top, bottom = y == 0, y == self.maze_height
        left, right = x == 0, x == self.maze_width
        if (top or bottom) and (left or right):
            return "double_corner", self.ARC_AROUND[position]

        if top:
            rotation = Rotation.R0
            opposite = "down"
            possible_tiles = {
                "BR": "line_and_corner_left",
                "BL": "line_and_corner_right"
            }

        elif bottom:
            rotation = Rotation.R180
            opposite = "up"
            possible_tiles = {
                "TR": "line_and_corner_right",
                "TL": "line_and_corner_left"
            }

        elif left:
            rotation = Rotation.R270
            opposite = "right"
            possible_tiles = {
                "BR": "line_and_corner_right",
                "TR": "line_and_corner_left"
            }

        else:
            rotation = Rotation.R90
            opposite = "left"
            possible_tiles = {
                "BL": "line_and_corner_left",
                "TL": "line_and_corner_right"
            }

        if walls[opposite]:
            return possible_tiles[position], rotation
        return "double_line", rotation

    def choose_normal_corner(
        self, position: str, walls: dict[str, bool]
    ) -> tuple[str, Rotation]:
        """Place the normal corners of the cells

        Args:
            position (str): the position of the corner relative to
            the adjacent cell
            walls (dict[str, bool]): Condition of the adjacent wall affecting
            the condition of the corner of this cell

        Returns:
            tuple[str, Rotation]: Return the cell name and correct the rotation
        """
        (
            vertical,
            horizontal,
            opposite_vertical,
            opposite_horizontal
        ) = self.NEIGHBORS[position]

        if walls[vertical] and walls[horizontal]:
            return "corner", self.ARC_AROUND[position]
        if walls[vertical]:
            return "line",  (
                Rotation.R90 if position in ("TL", "BL") else Rotation.R270
            )
        if walls[horizontal]:
            return "line",  (
                Rotation.R180 if position in ("TL", "TR") else Rotation.R0
            )
        if walls[opposite_vertical] or walls[opposite_horizontal]:
            return "corner", self.ARC_INSIDE[position]

        return ("black_tile", Rotation.R0)

    def choose_corner_tile(
        self, x: int, y: int, corner_x: int, corner_y: int
    ) -> tuple[str, Rotation]:
        """allows you to choose the right corner

        Args:
            x (int): the cell's coordinates (x)
            y (int): the cell's coordinates (y)
            corner_x (int): the tile's coordinates (x) in the cell
            corner_y (int): the tile's coordinates (y) in the cell

        Returns:
            tuple[str, Rotation]: Return the cell name and correct the rotation
        """
        position, dx, dy = self.CORNER_TILES[(corner_x, corner_y)]

        vx, vy = x + dx, y + dy
        walls = self.get_wall_by_neighbors(vx, vy)
        if vx in (0, self.maze_width) or vy in (0, self.maze_height):
            return self.choose_border_corner(vx, vy, position, walls)
        return self.choose_normal_corner(position, walls)

    def _choose_tiles(
        self, x: int, y: int
    ) -> list[list[tuple[str, Rotation]]]:
        """Selecting a cell returns the 9 corresponding tiles and
        their rotations

        Args:
            x (int): the cell's coordinates (x)
            y (int): the cell's coordinates (y)

        Returns:
            list[list[tuple[str, Rotation]]]: Return a matrix of the 9 tiles
            name with their rotations
        """
        side_coords = {
            (1, 0): (Direction.UP, Rotation.R0),
            (0, 1): (Direction.LEFT, Rotation.R270),
            (2, 1): (Direction.RIGHT, Rotation.R90),
            (1, 2): (Direction.DOWN, Rotation.R180)
        }
        tiles = [
            [("black_tile", Rotation.R0) for _ in range(3)] for _ in range(3)
            ]
        cell = self.maze[y][x]

        if self.is_full_cell(cell):
            return tiles

        for (sx, sy), (direction, rotation) in side_coords.items():
            if cell.there_is_wall(direction):
                if self._is_on_the_edge(sx, sy, x, y):
                    name = "double_line"
                else:
                    name = "line"
                tiles[sy][sx] = (name, rotation)

        for corner_x, corner_y in self.CORNER_TILES:
            tile = self.choose_corner_tile(x, y, corner_x, corner_y)
            tiles[corner_y][corner_x] = tile
        return tiles

    def create_maze_render(self, maze: list[list[Cell]], buffer: bytearray, buffer_pitch: int, zoom: int):
        """
        Create the buffer and fill it while staying within the maze walls
        """
        self.maze = maze

        self.maze_height = len(self.maze)
        self.maze_width = len(self.maze[0])

        for maze_y in range(self.maze_height):
            for maze_x in range(self.maze_width):
                tile_size = self.spritesheet.spritesheet_config.tile_size

                tiles = self._choose_tiles(maze_x, maze_y)

                for sub_y in [maze_y * 3, maze_y * 3 + 1, maze_y * 3 + 2]:
                    for sub_x in [maze_x * 3, maze_x * 3 + 1, maze_x * 3 + 2]:
                        tile_name, rotation = tiles[sub_y % 3][sub_x % 3]
                        tile = self.spritesheet.take_tiles(tile_name)[0]
                        tile = self.spritesheet.rotate_tile(tile, rotation)

                        self.spritesheet.copy_tile_into_buffer(
                            buffer,
                            buffer_pitch,
                            tile,
                            sub_x * tile_size,
                            sub_y * tile_size,
                            zoom
                        )
        # return self.buffer
