from src.utils.widget.widget import Widget, make_text_layer, Align
from src.utils.sprite_sheet_manager import SpriteSheetManager


class Label(Widget):
    def __init__(
        self,
        text: str,
        zoom: int,
        font: SpriteSheetManager,
        color: tuple[int, int, int],
        *,
        x: int = 0,
        y: int = 0,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        blink_period: float | None = None,
        align: Align = "center",
    ) -> None:
        self.layer = make_text_layer(text, zoom, font, color, align)
        super().__init__(
            self.layer.width,
            self.layer.height,
            x=x,
            y=y,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            blink_period=blink_period,
        )

    def _render(self) -> None:
        self.layer.draw(self.left, self.bottom)
