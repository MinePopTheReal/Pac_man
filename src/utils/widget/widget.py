from src.utils.sprite_sheet_manager import SpriteSheetManager
from src.utils.text_renderer import TextRenderer
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
    lines = text.splitlines() or [""]
    columns = max(len(line) for line in lines)
    layer = Layer(columns * zoom, len(lines) * zoom, "RGBA")
    factor = _ALIGN_FACTOR[align]
    for row, line in enumerate(lines):
        start = int((columns - len(line)) * factor)
        TextRenderer.draw_string(
            layer.buffer_view, line, start, row, zoom, font, color
        )
    return layer


class Widget:
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
        return round(self.x - self.anchor_x * self.width)

    @property
    def bottom(self) -> int:
        return round(self.y - self.anchor_y * self.height)

    def update(self, dt: float) -> None:
        if self.blink_period:
            self.timer += dt
            self.visible = (
                self.timer % (2 * self.blink_period)
            ) < self.blink_period

    def draw(self) -> None:
        if self.visible:
            self._render()

    def _render(self) -> None:
        raise NotImplementedError
