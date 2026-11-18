from src.rendering.sprite_sheet_manager import SpriteSheetManager
from src.rendering.sprite_sheet_manager import Rotation
from src.message.errors import RenderError


from pyglet import display, window
from dataclasses import dataclass
from functools import cache

# Consistency in size, colors, magnification
# factor, etc., to ensure a consistent display


# text color
TOP1_COLOR = (212, 175, 55)
TOP2_COLOR = (192, 192, 192)
TOP3_COLOR = (205, 127, 50)
MAJOR_COLOR = (255, 255, 0)
MINOR_COLOR = (245, 245, 220)

# screen & text size
SCREEN_MARGIN = 0.95
REFERENCE_RESOLUTION = (3840 * SCREEN_MARGIN, 2160 * SCREEN_MARGIN)
MINIMAL_RESOLUTION = (854 * SCREEN_MARGIN, 480 * SCREEN_MARGIN)

@cache
def get_actual_resolution() -> tuple[int, int]:
    """Return the screen resolution, or raise RenderError if no screen."""
    try:
        screen = display.get_display().get_default_screen()
    except window.NoSuchDisplayException as e:
        raise RenderError(
            "No display available: cannot read the screen resolution"
        ) from e
    return screen.width, screen.height

@dataclass(frozen=True)
class Layout:
    """Everything that depends on the screen resolution."""
    width: int
    height: int
    scale_factor: float
    h1_px_size: int
    h2_px_size: int
    h3_px_size: int
    h4_px_size: int
    h5_px_size: int
    h6_px_size: int


def compute_layout() -> Layout:
    """Read the screen and compute every size that depends on it."""
    screen_width, screen_height = get_actual_resolution()
    width = int(screen_width * SCREEN_MARGIN)
    height = int(screen_height * SCREEN_MARGIN)
    scale = max(0.1, min(
        width / REFERENCE_RESOLUTION[0],
        height / REFERENCE_RESOLUTION[1],
    ))
    return Layout(
        width, height, scale,
        int(250 * scale),
        int(75 * scale),
        int(75 * scale),
        int(40 * scale),
        int(25 * scale),
        int(10 * scale),
    )

class Assets:
    """
    Pre-loaded sprites and all kinds of useful information for rendering
    """
    def __init__(self, layout: Layout) -> None:

        self.layout = layout

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

        self.window_width = self.layout.width
        self.window_height = self.layout.height

        ps = self.font_spritesheet.preloading_sprites
        ps([Rotation.R0], self.layout.h1_px_size)
        ps([Rotation.R0], self.layout.h2_px_size)
        ps([Rotation.R0], self.layout.h3_px_size)
        ps([Rotation.R0], self.layout.h4_px_size)
        ps([Rotation.R0], self.layout.h5_px_size)
        ps([Rotation.R0], self.layout.h6_px_size)
