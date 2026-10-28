from enum import IntEnum
from PIL import Image
from numpy import asarray, ndarray, rot90

from src.parsing.parse_config import ConfigParser
from src.parsing.models import Spritesheet


class Rotation(IntEnum):
    R0 = 0
    R90 = 90
    R180 = 180
    R270 = 270


class SpriteSheetManager:
    """
    A utility function for taking a sprite sheet and manipulating its sprites
    """

    def __init__(self, config_path: str, image_path: str, format: str) -> None:
        self.format: str = format
        self.bytes_number_per_pixel: int = len(self.format)

        self.rotation_to_numpy_rotation = {
            Rotation.R90: -1,
            Rotation.R180: 2,
            Rotation.R270: 1,
        }

        self.spritesheet_config: Spritesheet = self._load_spritesheet_config(
            config_path
        )
        self.spritesheet_bytes: ndarray = self._load_spritesheet(image_path)

        self.sprites_bytes: dict[int, dict[str, dict[Rotation, list[ndarray]]]] = {}

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

    def _load_spritesheet(self, image_path: str) -> ndarray:
        """Load a sprite sheet

        Args:
            image_path (str):  The path to the sprite sheet

        Returns:
            ndarray: Return an array containing all the pixels in the
            sprite sheet
        """
        image = Image.open(image_path).convert(self.format)

        pixels = asarray(image)
        return pixels

    def preloading_sprites(
        self, rotation_to_load: list[Rotation], zoom: int
    ) -> None:
        """
        Allows you to preload all sprites while taking into account the
        zoom level and user-specified rotation, so you don't have to rework
        or transform the tiles later, thereby improving performance.

        Args:
            rotation_to_load (list[Rotation]): rotation list, to rotate
            the sprites based on the user's needs
            zoom (int): zooming in on the buffer to get adapted sprites
        """
        if zoom in self.sprites_bytes.keys():
            return
        ts = self.spritesheet_config.tile_size

        sprites_bytes = {}
        for name, coords in self.spritesheet_config.tiles.items():
            sprites = {}
            for rotation in rotation_to_load:
                frames = []
                for coord in coords:
                    sprite = self.spritesheet_bytes[
                        coord.y:coord.y + ts, coord.x:coord.x + ts
                    ]
                    zoomed_sprite = sprite.repeat(zoom, 0).repeat(zoom, 1)
                    frames.append(self.rotate_sprites(zoomed_sprite, rotation))
                sprites[rotation] = frames
            sprites_bytes[name] = sprites
        self.sprites_bytes[zoom] = sprites_bytes

    def rotate_sprites(
        self, sprite_bytes: ndarray, rotation: Rotation
    ) -> ndarray:
        """rotate the sprites

        Args:
            sprite_bytes (ndarray): Pixel-by-pixel representation of the sprite
            rotation (Rotation): desired rotation

        Returns:
            ndarray: rotate the sprite
        """
        if rotation == Rotation.R0:
            return sprite_bytes

        return rot90(sprite_bytes, self.rotation_to_numpy_rotation[rotation])

    def copy_tile_into_buffer(
        self,
        buffer_view: ndarray,
        tile_name: str,
        rotation: Rotation,
        x: int,
        y: int,
        zoom: int,
        frame: int,
    ) -> None:
        """
        Copy the tile to the buffer in the correct location

        Args:
            buffer_view (ndarray): the buffer view (NumPy object) to
            simplify calculations

            tile_name (str): the tile name
            rotation (Rotation): the desired rotation of the tile in the buffer
            x (int): coordinate (x) of the tile in the buffer (in pixels)
            y (int): coordinate (y) of the tile in the buffer (in pixels)
            zoom (int): the zoom
            frame (int): the frame number in the animation
        """
        ts = self.spritesheet_config.tile_size * zoom
        sprite = self.sprites_bytes[zoom][tile_name][rotation][
            frame % len(self.sprites_bytes[zoom][tile_name][rotation])
        ]
        if sprite.shape[2] == 4:
            mask = sprite[:, :, 3] > 0
            buffer_view[y:y + ts, x:x + ts][mask] = sprite[mask]
        else:
            buffer_view[y:y + ts, x:x + ts] = sprite
