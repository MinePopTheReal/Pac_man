from src.rendering.sprite_sheet_manager import SpriteSheetManager
from src.rendering.sprite_sheet_manager import Rotation


from pyglet import display


# Consistency in size, colors, magnification
# factor, etc., to ensure a consistent display


# screen
SCREEN_MARGIN = 0.95

REFERENCE_RESOLUTION = (3840 * SCREEN_MARGIN, 2160 * SCREEN_MARGIN)
SCREEN = display.get_display().get_default_screen()

ACTUAL_RESOLUTION = (
    int(SCREEN.width * SCREEN_MARGIN),
    int(SCREEN.height * SCREEN_MARGIN),
)

SCALE_FACTOR = max(
    0.1,
    min(
        ACTUAL_RESOLUTION[0] / REFERENCE_RESOLUTION[0],
        ACTUAL_RESOLUTION[1] / REFERENCE_RESOLUTION[1],
    ),
)

MINIMAL_RESOLUTION = (854 * SCREEN_MARGIN, 480 * SCREEN_MARGIN)

# sprite size
WALL_SIZE = int(24 * SCALE_FACTOR)
ENTITIES_SIZE = WALL_SIZE * 2

H1_PX_SIZE = int(250 * SCALE_FACTOR)
H2_PX_SIZE = int(75 * SCALE_FACTOR)
H3_PX_SIZE = int(75 * SCALE_FACTOR)
H4_PX_SIZE = int(40 * SCALE_FACTOR)
H5_PX_SIZE = int(25 * SCALE_FACTOR)
H6_PX_SIZE = int(10 * SCALE_FACTOR)

# text color
TOP1_COLOR = (212, 175, 55)
TOP2_COLOR = (192, 192, 192)
TOP3_COLOR = (205, 127, 50)
MAJOR_COLOR = (255, 255, 0)
MINOR_COLOR = (245, 245, 220)


class Assets:
    """
    Pre-loaded sprites and all kinds of useful information for rendering
    """
    def __init__(self, window_width: int, window_height: int) -> None:
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

        ps = self.font_spritesheet.preloading_sprites
        ps([Rotation.R0], H1_PX_SIZE)
        ps([Rotation.R0], H2_PX_SIZE)
        ps([Rotation.R0], H3_PX_SIZE)
        ps([Rotation.R0], H4_PX_SIZE)
        ps([Rotation.R0], H5_PX_SIZE)
        ps([Rotation.R0], H6_PX_SIZE)
