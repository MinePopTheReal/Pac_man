from src.utils.sprite_sheet_manager import SpriteSheetManager
from src.utils.sprite_sheet_manager import Rotation

HUD_ZOOM = 2
TITLE_ZOOM = 30
MENU_ZOOM = 15


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
        self.font_y_spritesheet = SpriteSheetManager(
            "assets/font_spritesheet_config.json",
            "assets/font_y_spritesheet.png",
            "RGBA",
        )
        self.font_w_spritesheet = SpriteSheetManager(
            "assets/font_spritesheet_config.json",
            "assets/font_w_spritesheet.png",
            "RGBA",
        )

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.window_width = window_width
        self.window_height = window_height


        self.font_y_spritesheet.preloading_sprites([Rotation.R0], TITLE_ZOOM)
        self.font_w_spritesheet.preloading_sprites([Rotation.R0], MENU_ZOOM)
        self.font_y_spritesheet.preloading_sprites([Rotation.R0], MENU_ZOOM)