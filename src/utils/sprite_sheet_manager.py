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

        pixels = asarray(image)
        return pixels

    def preloading_sprites(self, rotation_to_load: list[Rotation], zoom: int):
        ts = self.spritesheet_config.tile_size

        for name, coords in self.spritesheet_config.tiles.items():
            sprites = {}
            for rotation in rotation_to_load:
                frames = []
                for coord in coords:
                    sprite = self.spritesheet_bytes[coord.y:coord.y + ts, coord.x:coord.x + ts]
                    zoomed_sprite = sprite.repeat(zoom, 0).repeat(zoom, 1)
                    frames.append(self.rotate_sprites(zoomed_sprite, rotation))
                sprites[rotation] = frames
            self.sprites_bytes[name] = sprites

    def rotate_sprites(self, sprite_bytes: ndarray, rotation: Rotation):

        if rotation == Rotation.R0:
            return sprite_bytes

        return rot90(sprite_bytes, self.rotation_to_numpy_rotation[rotation])

    def copy_tile_into_buffer(self, buffer_view, tile_name, rotation, x, y, zoom, frame):
        ts = self.spritesheet_config.tile_size * zoom
        sprite = self.sprites_bytes[tile_name][rotation][frame % len(self.sprites_bytes[tile_name][rotation])]
        if sprite.shape[2] == 4:
            mask = sprite[:, :, 3] > 0
            buffer_view[y:y + ts, x:x + ts][mask] = sprite[mask]
        else:
            buffer_view[y:y + ts, x:x + ts] = sprite
