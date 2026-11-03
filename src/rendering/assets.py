from src.utils.sprite_sheet_manager import SpriteSheetManager
from src.utils.sprite_sheet_manager import Rotation
from src.rendering.display import SCALE_FACTOR

# SCALE_FACTOR

# sprite size
WALL_SIZE = int(24 * SCALE_FACTOR)
ENTITIES_SIZE = WALL_SIZE * 2

H1_PX_SIZE = int(250 * SCALE_FACTOR)
H2_PX_SIZE = int(75 * SCALE_FACTOR)
H3_PX_SIZE = int(75 * SCALE_FACTOR)
H4_PX_SIZE = int(50 * SCALE_FACTOR)
H5_PX_SIZE = int(25 * SCALE_FACTOR)
H6_PX_SIZE = int(10 * SCALE_FACTOR)

# H3_PX_SIZE = int(50 * SCALE_FACTOR)
# H3_PX_SIZE = int(75 * SCALE_FACTOR)
# H1_PX_SIZE = int(250 * SCALE_FACTOR)

# text margin
TITLE_MARGIN = 0.6

# text color
TOP1_COLOR = (212, 175, 55)
TOP2_COLOR = (192, 192, 192)
TOP3_COLOR = (205, 127, 50)
MAJOR_COLOR = (255, 255, 0)
MINOR_COLOR = (245, 245, 220)

class Assets:
    def __init__(self, window_width, window_height):
        self.wall_spritesheet = SpriteSheetManager(
            "assets/wall_spritesheet_config.json",
            "assets/wall_spritesheet.png",
            "RGB",
        )
        self.entities_spritesheet = SpriteSheetManager(
            "assets/entities_spritesheet_config.json",
            "assets/entities_spritesheet.png",
            "RGBA",
        )
        self.font_spritesheet = SpriteSheetManager(
            "assets/font_spritesheet_config.json",
            "assets/font_spritesheet.png",
            "RGBA",
        )

        self.window_width = window_width
        self.window_height = window_height


        self.font_spritesheet.preloading_sprites([Rotation.R0], H1_PX_SIZE)
        self.font_spritesheet.preloading_sprites([Rotation.R0], H2_PX_SIZE)
        self.font_spritesheet.preloading_sprites([Rotation.R0], H3_PX_SIZE)
        self.font_spritesheet.preloading_sprites([Rotation.R0], H4_PX_SIZE)
        self.font_spritesheet.preloading_sprites([Rotation.R0], H5_PX_SIZE)
        self.font_spritesheet.preloading_sprites([Rotation.R0], H6_PX_SIZE)
        