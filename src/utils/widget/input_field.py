from src.utils.sprite_sheet_manager import SpriteSheetManager
from src.utils.text_renderer import TextRenderer
from src.utils.widget.widget import Widget
from src.rendering.layer import Layer


MAX_NAME_LENGTH = 10


class InputField(Widget):
    def __init__(
        self,
        prompt: str,
        zoom: int,
        font: SpriteSheetManager,
        color_prompt: tuple[int, int, int],
        color_text: tuple[int, int, int],
        *,
        x: int = 0,
        y: int = 0,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        blink_period: float | None = None,
    ) -> None:
        super().__init__(
            max(len(prompt), MAX_NAME_LENGTH) * zoom,
            zoom * 2,
            x=x,
            y=y,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            blink_period=blink_period,
        )
        self.prompt = prompt
        self.zoom = zoom
        self.font = font
        self.color_prompt = color_prompt
        self.color_text = color_text
        self.layer = Layer(self.width, self.height, "RGBA")
        self._text: str | None = None
        self.set_text("")

    def set_text(self, text: str) -> None:
        if text == self._text:
            return
        self._text = text
        self.layer.clear()
        TextRenderer.draw_string(
            self.layer.buffer_view,
            self.prompt,
            0,
            0,
            self.zoom,
            self.font,
            self.color_prompt,
        )
        TextRenderer.draw_string(
            self.layer.buffer_view,
            text,
            ((self.layer.width // self.zoom) // 2) - (len(text) // 2),
            1,
            self.zoom,
            self.font,
            self.color_text,
        )

    def _render(self) -> None:
        self.layer.draw(self.left, self.bottom)
