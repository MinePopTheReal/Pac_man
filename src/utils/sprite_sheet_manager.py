from enum import IntEnum
from PIL import Image

from src.parsing.parse_config import ConfigParser
from src.parsing.models import Spritesheet


class Rotation(IntEnum):
    R0 = 0
    R90 = 90
    R180 = 180
    R270 = 270


class SpriteSheetManager():
    """
    A utility function for taking a sprite sheet and manipulating its sprites
    """    
    def __init__(self, config_path: str, image_path: str) -> None:
        self.format = "RGB"
        self.bytes_number_per_pixel: int = len(self.format)

        self.spritesheet_config: Spritesheet = self._load_spritesheet_config(
            config_path
        )
        self.spritesheet, self.pitch, = self._load_spritesheet(image_path)

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

        width, _ = image.size
        pixels = image.tobytes()
        pitch = -width * self.bytes_number_per_pixel

        return pixels, pitch

    def _R90(self, x: int, y: int) -> tuple[int, int]:
        """Formula for calculating the new coordinates of a pixel from an
        image in order to rotate it by 90 degrees

        Args:
            x (int): x-coordinate of the pixel
            y (int): y-coordinate of the pixel

        Returns:
            tuple[int, int]: News coordinates
        """        
        return (self.spritesheet_config.tile_size - 1 - y, x)

    def _R180(self, x: int, y: int) -> tuple[int, int]:
        """Formula for calculating the new coordinates of a pixel from an
        image in order to rotate it by 180 degrees

        Args:
            x (int): x-coordinate of the pixel
            y (int): y-coordinate of the pixel

        Returns:
            tuple[int, int]: News coordinates
        """        
        return (
            self.spritesheet_config.tile_size - 1 - x,
            self.spritesheet_config.tile_size - 1 - y
            )

    def _R270(self, x: int, y: int) -> tuple[int, int]:
        """Formula for calculating the new coordinates of a pixel from an
        image in order to rotate it by 270 degrees

        Args:
            x (int): x-coordinate of the pixel
            y (int): y-coordinate of the pixel

        Returns:
            tuple[int, int]: News coordinates
        """        
        return (y, self.spritesheet_config.tile_size - 1 - x)

    def rotate_tile(self, bytes_tile: bytearray, rotation: Rotation):
        """Rotate a tile completely according to the requested degree

        Args:
            bytes_tile (bytearray): the tile
            rotation (Rotation): the degrees

        Returns:
            bytearray: th tile with rotation
        """        
        tile_size = self.spritesheet_config.tile_size
        temp_tile: bytearray = bytearray(tile_size * 3 * tile_size)
        bpp = self.bytes_number_per_pixel

        if rotation == Rotation.R0:
            return bytes_tile

        formula = {
            Rotation.R90: self._R90,
            Rotation.R180: self._R180,
            Rotation.R270: self._R270
        }

        for y_px in range(tile_size):
            for x_px in range(tile_size):
                pitch = (
                    y_px
                    * tile_size
                    * bpp
                    )
                pixel_data = bytes_tile[
                    x_px * bpp + pitch:x_px * bpp + pitch + bpp
                    ]

                new_x, new_y = formula[rotation](x_px, y_px)
                new_pitch = new_y * tile_size * bpp
                temp_tile[
                    new_x * bpp + new_pitch:new_x * bpp + new_pitch + bpp
                    ] = pixel_data
        return temp_tile

    def take_tile(self, tile_name: str) -> bytearray:
        """Retrieve a tile from the sprite sheet using the configuration
        and the image

        Args:
            tile_name (str): the tile's name

        Returns:
            bytearray: the tile
        """        
        temp_tile: bytearray = bytearray()

        coord = self.spritesheet_config.tiles[tile_name][0]
        bpp = self.bytes_number_per_pixel
        tile_size = self.spritesheet_config.tile_size

        for y_px in range(tile_size):
            position = (coord.y + y_px) * abs(self.pitch) + coord.x * bpp
            temp_tile += bytearray(
                self.spritesheet[position:position + tile_size * bpp]
                )
        return temp_tile

    def copy_tile_into_buffer(
        self,
        buffer: bytearray,
        buffer_pitch: int,
        tile: bytearray,
        buffer_x: int,
        buffer_y: int
    ) -> None:
        """Allows you to copy a tile into a larger buffer
        that is modified directly

        Args:
            buffer (bytearray): the buffer
            buffer_pitch (int): the buffer pitch (one line of the 
            image in bytes)
            tile (bytearray): the tile to copy to the clipboard
            buffer_x (int): the coordinates (x) in the buffer to place the tile
            buffer_y (int): the coordinates (y) in the buffer to place the tile
        """        
        tile_size = self.spritesheet_config.tile_size
        bpp = self.bytes_number_per_pixel

        for y_px in range(tile_size):
            tile_pitch = y_px * tile_size * bpp
            position = (buffer_y + y_px) * abs(buffer_pitch) + buffer_x * bpp
            buffer[
                position:position + tile_size * bpp
                ] = tile[tile_pitch:tile_pitch + tile_size * bpp]
