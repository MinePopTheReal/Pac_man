from src.rendering.sprite_sheet_manager import SpriteSheetManager, Rotation
from src.message.errors import RenderError


from numpy import ndarray


def draw_string(
    buffer_view: ndarray,
    string: str,
    x: int,
    y: int,
    zoom: int,
    spritesheet: SpriteSheetManager,
    color: tuple[int, int, int] = (255, 255, 255),
) -> None:
    """
    It creates the output of a string, displaying
    it character by character.
    Args:
        string (str): the string to display
        x (int): the coordinates (x) of the beginning of the text (offset
        equal to the size of one character)
        y (int): the coordinates (y) of the beginning of the text (offset
        equal to the size of one character)
    """

    new_y = y * zoom
    for index, letter in enumerate(string.upper()):
        if letter in [" "]:
            continue
        new_x = (x + index) * zoom
        try:
            spritesheet.copy_tile_into_buffer(
                buffer_view,
                letter,
                Rotation.R0,
                new_x, new_y,
                zoom,
                0,
                color
            )
        except RenderError:
            raise RenderError(
                "One of the characters in the string to be displayed "
                "does not exist in the sprite sheet"
            )
