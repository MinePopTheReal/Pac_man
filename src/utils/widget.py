from typing import Protocol

from src.rendering.layer import Layer
from src.utils.text_renderer import TextRenderer
from src.utils.highscore_manager import MAX_SCORES, MAX_NAME_LENGTH
from src.rendering.assets import MENU_ZOOM


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
        TextRenderer.draw_string(
            self.layer.buffer_view,
            text,
            0,
            0,
            zoom,
            font,
            color
        )
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
            self.visible = (
                self.timer % (2 * self.blink_period)
            ) < self.blink_period

    def draw(self) -> None:
        if self.visible:
            self.layer.draw(
                round(self.x - self.anchor_x * self.width),
                round(self.y - self.anchor_y * self.height)
            )

class MenuItem:
    def __init__(self, text: str, zoom: int, font, normal_color, selected_color) -> None:
        self.width = len(text) * zoom
        self.normal = Layer(self.width, zoom, "RGBA")
        self.selected = Layer(self.width, zoom, "RGBA")
        TextRenderer.draw_string(self.normal.buffer_view, text, 0, 0, zoom, font, normal_color)
        TextRenderer.draw_string(self.selected.buffer_view, text, 0, 0, zoom, font, selected_color)

    def draw(self, x: int, y: int, is_selected: bool) -> None:
        (self.selected if is_selected else self.normal).draw(x, y)

class Menu:
    def __init__(
        self,
        texts: list[str],
        zoom: int,
        font,
        normal_color,
        selected_color,
        *,
        x: int,
        y: int,
        anchor_x: float = 0.5,
        anchor_y: float = 0.5,
    ) -> None:
        self.items = [MenuItem(t, zoom, font, normal_color, selected_color) for t in texts]
        self.x, self.y = x, y
        self.anchor_x, self.anchor_y = anchor_x, anchor_y
        self.zoom = zoom
        self.gap = zoom
        self.width = max(item.width for item in self.items)
        n = len(self.items)
        self.height = n * zoom + (n - 1) * self.gap

    def update(self, dt: float) -> None:
        pass

    def draw(self, selected: int = 0) -> None:
        left = round(self.x - self.anchor_x * self.width)
        top = round(self.y - self.anchor_y * self.height) + self.height
        for i, item in enumerate(self.items):
            item_x = left + (self.width - item.width) // 2
            item_y = top - self.zoom - i * (self.zoom + self.gap)
            item.draw(item_x, item_y, i == selected)

SCORE_DIGITS = 10

class HighscoresLabel:
    def __init__(
        self, 
        zoom: int, 
        font, 
        top1_color, 
        top2_color, 
        top3_color, 
        normal_color,
        *, 
        x: int = 0, 
        y: int = 0, 
        anchor_x: float = 0.0, 
        anchor_y: float = 0.0
    ) -> None:
        self.zoom = zoom
        self.font = font
        self.rank_colors = [top1_color, top2_color, top3_color]
        self.normal_color = normal_color
        self.x, self.y = x, y
        self.anchor_x, self.anchor_y = anchor_x, anchor_y

        chars = 3 + 1 + MAX_NAME_LENGTH + 1 + SCORE_DIGITS 
        self.layer = Layer(chars * zoom, MAX_SCORES * zoom, "RGBA")
        self.width = self.layer.width
        self.height = self.layer.height

        self._drawn: list[tuple[str, int]] | None = None

    def set_scores(self, scores: list[tuple[str, int]]) -> None:
        if scores == self._drawn:
            return
        self._drawn = list(scores)
        self.layer.clear()
        for rank in range(MAX_SCORES):
            username, score = scores[rank] if rank < len(scores) else ('-', '-')
            color = self.rank_colors[rank] if rank < len(self.rank_colors) and rank < len(scores) \
                else self.normal_color
            TextRenderer.draw_string(
                self.layer.buffer_view,
                f"{rank + 1:>3}.{username:<{MAX_NAME_LENGTH}} {score}",
                0, rank, self.zoom, self.font, color,
            )

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        self.layer.draw(
            round(self.x - self.anchor_x * self.width),
            round(self.y - self.anchor_y * self.height),
        )

class InputField:
    def __init__(
        self,
        prompt: str,
        zoom: int,
        font,
        color_prompt,
        color_text,
        *,
        x: int = 0,
        y: int = 0,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
    ) -> None:
        self.layer = Layer(max(len(prompt), MAX_NAME_LENGTH) * zoom, zoom * 2, "RGBA")

        self.prompt = prompt

        self.font = font
        self.color_prompt = color_prompt
        self.color_text = color_text
        

        self.x, self.y = x, y
        self.anchor_x, self.anchor_y = anchor_x, anchor_y
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
            self.visible = (
                self.timer % (2 * self.blink_period)
            ) < self.blink_period

    def draw(self, text) -> None:
        self.layer.clear()
        if self.visible:
            TextRenderer.draw_string(
                self.layer.buffer_view,
                self.prompt,
                0,
                0,
                MENU_ZOOM,
                self.font,
                self.color_prompt
            )
            TextRenderer.draw_string(
                self.layer.buffer_view,
                text,
                0,
                1,
                MENU_ZOOM,
                self.font,
                self.color_text
            )
            self.layer.draw(
                round(self.x - self.anchor_x * self.width),
                round(self.y - self.anchor_y * self.height)
            )
