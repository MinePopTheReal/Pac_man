from src.rendering.sprite_sheet_manager import SpriteSheetManager
from src.rendering.text_drawing import draw_string
from src.rendering.layer import Layer


from typing import Literal


Align = Literal["left", "center", "right"]
_ALIGN_FACTOR: dict[Align, float] = {
    "left": 0.0,
    "center": 0.5,
    "right": 1.0
}


def make_text_layer(
    text: str,
    zoom: int,
    font: SpriteSheetManager,
    color: tuple[int, int, int],
    align: Align = "center"
) -> Layer:
    """Draw a text, which can have several lines, into a new layer.

    The layer is exactly as big as the text: as wide as the longest
    line and as high as the number of lines. The shorter lines are
    placed according to the alignment.
    """
    lines = text.splitlines() or [""]
    columns = max(len(line) for line in lines)
    layer = Layer(columns * zoom, len(lines) * zoom, "RGBA")
    factor = _ALIGN_FACTOR[align]
    for row, line in enumerate(lines):
        start = int((columns - len(line)) * factor)
        draw_string(
            layer.buffer_view, line, start, row, zoom, font, color
        )
    return layer


class Widget:
    """Base class of everything drawn on a screen (text, menu, maze...).

    A widget has a size and a position. The position is given by an
    anchor point: x and y are the coordinates in the window of the point
    of the widget placed by anchor_x and anchor_y. It can also blink.
    A subclass only has to write _render(), which draws its content.

    The origin of the window is at the bottom left, so a larger y is
    higher.
    """
    def __init__(
        self,
        width: int,
        height: int,
        *,
        x: int = 0,
        y: int = 0,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        blink_period: float | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.x, self.y = x, y
        self.anchor_x, self.anchor_y = anchor_x, anchor_y
        self.blink_period = blink_period
        self.timer = 0.0
        self.visible = True

    @property
    def left(self) -> int:
        """X coordinate of the left side of the widget, in pixels."""
        return round(self.x - self.anchor_x * self.width)

    @property
    def bottom(self) -> int:
        """Y coordinate of the bottom side of the widget, in pixels."""
        return round(self.y - self.anchor_y * self.height)

    def update(self, dt: float) -> None:
        """Make the blinking move forward.

        The widget is shown during blink_period seconds, then hidden
        during the same time, and so on. Does nothing if the widget does
        not blink. It is not called automatically: the screen that owns
        the widget must call it each frame.

        Args:
            dt (float): Seconds since the last frame.
        """
        if self.blink_period:
            self.timer += dt
            self.visible = (
                self.timer % (2 * self.blink_period)
            ) < self.blink_period

    def draw(self) -> None:
        """Draw the widget in the window, unless it is hidden."""
        if self.visible:
            self._render()

    def _render(self) -> None:
        """Draw the content of the widget.

        Called by draw() when the widget is visible. Each subclass must
        override it.

        Raises:
            NotImplementedError: If the subclass did not override it.
        """
        raise NotImplementedError
