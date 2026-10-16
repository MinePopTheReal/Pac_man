from enum import IntEnum
from PIL import Image
from numpy import asarray, ndarray, rot90, set_printoptions

from src.parsing.parse_config import ConfigParser
from src.parsing.models import Spritesheet

import sys

set_printoptions(threshold=sys.maxsize)

class Rotation(IntEnum):
    R0 = 0
    R90 = 90
    R180 = 180
    R270 = 270


class SpriteSheetManager():
    """
    A utility function for taking a sprite sheet and manipulating its sprites
    """    
    def __init__(self, config_path: str, image_path: str, format: str) -> None:
        self.format: str = format
        self.bytes_number_per_pixel: int = len(self.format)

        self.rotation_to_numpy_rotation = {
            Rotation.R90: -1,
            Rotation.R180: 2,
            Rotation.R270: 1
        }

        self.spritesheet_config: Spritesheet = self._load_spritesheet_config(
            config_path
        )
        self.spritesheet_bytes: ndarray = self._load_spritesheet(image_path)

        self.sprites_bytes: dict[str, dict[Rotation, list[ndarray]]] = {}

    def _load_spritesheet_config(self, config_path: str) -> Spritesheet:
        """
        Load the configuration associated with the sprite sheet

        Args:
            config_path (str): The path to the sprite sheet configuration

        Returns:
            Spritesheet: A spritesheet object containing the entire
            sprite configuration
        """        
        parser = ConfigParser()
        spritesheet = parser.load_config(config_path, Spritesheet)
        return spritesheet

    def _load_spritesheet(self, image_path: str) -> tuple[bytes, int]:
        """Load a sprite sheet 

        Args:
            image_path (str): The path to the sprite sheet

        Returns:
            tuple[bytes, int]: Returns the necessary bytes for each pixel as
            well as the image pitch
        """        
        image = Image.open(image_path).convert(self.format)

        # opti test
        pixels = asarray(image)
        return pixels
        # width, _ = image.size
        # pixels = image.tobytes()
        # pitch = -width * self.bytes_number_per_pixel

        # return pixels, pitch

    def preloading_sprites(self, rotation_to_load: list[Rotation], zoom: int):
        ts = self.spritesheet_config.tile_size

        for name, coords in self.spritesheet_config.tiles.items():
            sprites = {}
            for rotation in rotation_to_load:
                frames = []
                for coord in coords:
                    sprite = self.spritesheet_bytes[coord.x:coord.x + ts, coord.y:coord.y + ts]
                    zoomed_sprite = sprite.repeat(zoom, 0).repeat(zoom, 1)
                    frames.append(self.rotate_sprites(zoomed_sprite, rotation))
                sprites[rotation] = frames
            self.sprites_bytes[name] = frames

    # def _R90(self, x: int, y: int, tile_size: int) -> tuple[int, int]:
    #     """Formula for calculating the new coordinates of a pixel from an
    #     image in order to rotate it by 90 degrees

    #     Args:
    #         x (int): x-coordinate of the pixel
    #         y (int): y-coordinate of the pixel

    #     Returns:
    #         tuple[int, int]: News coordinates
    #     """        
    #     return (tile_size - 1 - y, x)

    # def _R180(self, x: int, y: int, tile_size: int) -> tuple[int, int]:
    #     """Formula for calculating the new coordinates of a pixel from an
    #     image in order to rotate it by 180 degrees

    #     Args:
    #         x (int): x-coordinate of the pixel
    #         y (int): y-coordinate of the pixel

    #     Returns:
    #         tuple[int, int]: News coordinates
    #     """        
    #     return (
    #         tile_size - 1 - x,
    #         tile_size - 1 - y
    #         )

    # def _R270(self, x: int, y: int, tile_size: int) -> tuple[int, int]:
    #     """Formula for calculating the new coordinates of a pixel from an
    #     image in order to rotate it by 270 degrees

    #     Args:
    #         x (int): x-coordinate of the pixel
    #         y (int): y-coordinate of the pixel

    #     Returns:
    #         tuple[int, int]: News coordinates
    #     """        
    #     return (y, tile_size - 1 - x)

    # def rotate_tile(self, bytes_tile: bytearray, rotation: Rotation, zoom: int):
    #     """Rotate a tile completely according to the requested degree

    #     Args:
    #         bytes_tile (bytearray): the tile
    #         rotation (Rotation): the degrees

    #     Returns:
    #         bytearray: th tile with rotation
    #     """        
    #     tile_size = self.spritesheet_config.tile_size * zoom
    #     temp_tile: bytearray = bytearray(tile_size * 3 * tile_size)
    #     bpp = self.bytes_number_per_pixel

    #     if rotation == Rotation.R0:
    #         return bytes_tile

    #     formula = {
    #         Rotation.R90: self._R90,
    #         Rotation.R180: self._R180,
    #         Rotation.R270: self._R270
    #     }

    #     for y_px in range(tile_size):
    #         for x_px in range(tile_size):
    #             pitch = (
    #                 y_px
    #                 * tile_size
    #                 * bpp
    #                 )
    #             pixel_data = bytes_tile[
    #                 x_px * bpp + pitch:x_px * bpp + pitch + bpp
    #                 ]

    #             new_x, new_y = formula[rotation](x_px, y_px, tile_size)
    #             new_pitch = new_y * tile_size * bpp
    #             temp_tile[
    #                 new_x * bpp + new_pitch:new_x * bpp + new_pitch + bpp
    #                 ] = pixel_data
    #     return temp_tile

    def rotate_sprites(self, sprite_bytes: ndarray, rotation: Rotation):

        if rotation == Rotation.R0:
            return sprite_bytes

        return rot90(sprite_bytes, self.rotation_to_numpy_rotation[rotation])

    # def take_tiles(self, tile_name: str, zoom: int) -> bytearray:
        # """Retrieve a tile from the sprite sheet using the configuration
        # and the image
# 
        # Args:
            # tile_name (str): the tile's name
# 
        # Returns:
            # bytearray: the tile
        # """

        # frames: list[bytearray] = []

        # bpp = self.bytes_number_per_pixel
        # tile_size = self.spritesheet_config.tile_size
        # pitch = abs(self.pitch)

        # for coord in self.spritesheet_config.tiles[tile_name]:
        #     temp_tile: bytearray = bytearray()
        #     for y_px in range(tile_size):
        #         start = (coord.y + y_px) * pitch + coord.x * bpp
        #         row = self.spritesheet[start:start + tile_size * bpp]
        #         zoomed_row = bytearray()
        #         for x_px in range(tile_size):
        #             pixel = row[x_px * bpp: (x_px + 1) * bpp]
        #             zoomed_row += pixel * zoom
        #         temp_tile += zoomed_row * zoom
        #     frames.append(temp_tile)

        # return frames

    def copy_tile_into_buffer(self, buffer_view, tile_name, rotation, x, y, zoom, frame):
        ts = self.spritesheet_config.tile_size * zoom
        buffer_view[y:y + ts, x, x + ts] = self.sprites_bytes[tile_name][rotation][frame % len(self.sprites_bytes[tile_name][rotation])]

    # def copy_tile_into_buffer(
    #     self,
    #     buffer: bytearray,
    #     buffer_pitch: int,
    #     tile: bytearray,
    #     x_px: float,
    #     y_px: float,
    #     zoom: int
    # ) -> None:
    #     """Allows you to copy a tile into a larger buffer
    #     that is modified directly

    #     Args:
    #         buffer (bytearray): the buffer
    #         buffer_pitch (int): the buffer pitch (one line of the 
    #         image in bytes)
    #         tile (bytearray): the tile to copy to the clipboard
    #         buffer_x (int): the coordinates (x) in the buffer to place the tile
    #         buffer_y (int): the coordinates (y) in the buffer to place the tile
    #     """
    #     tile_size = self.spritesheet_config.tile_size * zoom
    #     bpp = self.bytes_number_per_pixel
    #     for px in range(tile_size):
    #         tile_pitch = px * tile_size * bpp
    #         position = (y_px + px) * (abs(buffer_pitch)) + x_px * bpp
    #         buffer[
    #             position:position + tile_size * bpp
    #             ] = tile[tile_pitch:tile_pitch + tile_size * bpp]


# SpriteSheetManager(
#     "assets/entities_spritesheet_config.json", 
#     "assets/entities_spritesheet.png", 
#     "RGBA",
#     [Rotation.R180]
# )