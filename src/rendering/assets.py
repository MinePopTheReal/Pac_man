from src.utils.sprite_sheet_manager import SpriteSheetManager
from src.utils.sprite_sheet_manager import Rotation

# text zoom
HUD_ZOOM = 2
MENU_ZOOM = 10
TITLE_ZOOM = 30

# text margin
TITLE_MARGIN = 0.6

# text color
TOP1_COLOR = (212, 175, 55)
TOP2_COLOR = (192, 192, 192)
TOP3_COLOR = (205, 127, 50)
MAJOR_COLOR = (255, 255, 0)
MINOR_COLOR = (245, 245, 220)

class Assets:
    def __init__(self, screen_width, screen_height, window_width, window_height):
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

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.window_width = window_width
        self.window_height = window_height


        self.font_spritesheet.preloading_sprites([Rotation.R0], TITLE_ZOOM)
        self.font_spritesheet.preloading_sprites([Rotation.R0], MENU_ZOOM)