from typing import Protocol

from src.rendering.layer import Layer
from src.utils.text_renderer import TextRenderer

class Wiget(Protocol):
    def update(self, dt: float) -> None:
        ...

    def draw(self) -> None:
        ...

class Label:
    def __init__(
        self,
        text: str,
        zoom: int,
        font,
        color,
        *,
        x: int = 0,
        y: int = 0,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        blink_period: float | None = None,
    ) -> None:
        self.layer = Layer(len(text) * zoom, zoom, "RGBA")
        TextRenderer.draw_string(self.layer.buffer_view, text, 0, 0, zoom, font, color)
        self.x, self.y = x, y
        self.anchor_x, self.anchor_y = anchor_x, anchor_y
        self.blink_period = blink_period
        self.timer = 0.0
        self.visible = True

    @property
    def width(self) -> int:
        return self.layer.width

    @property
    def height(self) -> int:
        return self.layer.height

    def update(self, dt: float) -> None:
        if self.blink_period:
            self.timer += dt
            self.visible = (self.timer % (2 * self.blink_period)) < self.blink_period

    def draw(self) -> None:
        if self.visible:
            print(
                round(self.x - self.anchor_x * self.width),
                round(self.y - self.anchor_y * self.height)
                )
            self.layer.draw(
                round(self.x - self.anchor_x * self.width),
                round(self.y - self.anchor_y * self.height),
            )