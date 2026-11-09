from src.utils.sprite_sheet_manager import SpriteSheetManager
from src.utils.text_renderer import draw_string
from src.utils.widget.widget import Widget
from src.rendering.layer import Layer


MAX_NAME_LENGTH = 10


class InputField(Widget):
    """Widget that shows a prompt and, under it, the text typed by the player.

    The prompt is on the first line, aligned to the left. The text is on
    the second line, centered. The widget only displays the text: the key
    presses are handled by the screen, which gives the text to set_text().
    The content is drawn into its own layer, which is redrawn only when
    the text changes.
    """
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
        """Show a new text under the prompt.

        Does nothing if the text is the same as the last time, so it can
        be called every frame at no cost. The text is not limited here:
        it must fit in the width of the widget, so the caller has to
        limit its length (to MAX_NAME_LENGTH for a name).

        Args:
            text (str): The text to show, centered on the second line.
        """
        if text == self._text:
            return
        self._text = text
        self.layer.clear()
        draw_string(
            self.layer.buffer_view,
            self.prompt,
            0,
            0,
            self.zoom,
            self.font,
            self.color_prompt,
        )
        draw_string(
            self.layer.buffer_view,
            text,
            ((self.layer.width // self.zoom) // 2) - (len(text) // 2),
            1,
            self.zoom,
            self.font,
            self.color_text,
        )

    def _render(self) -> None:
        """Put the layer of the field in the window."""
        self.layer.draw(self.left, self.bottom)
