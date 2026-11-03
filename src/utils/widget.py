from src.rendering.layer import Layer
from src.utils.highscore_manager import MAX_NAME_LENGTH, MAX_SCORES
from src.utils.text_renderer import TextRenderer

SCORE_DIGITS = 10


def make_text_layer(text: str, zoom: int, font, color) -> Layer:
    lines = text.split('\n')
    layer = Layer(len(max(lines, key=lambda line: len(line))) * zoom, len(lines) * zoom, "RGBA")
    for y, line in enumerate(lines):
        TextRenderer.draw_string(layer.buffer_view, line, ((layer.width // zoom) // 2) - (len(line) // 2), y, zoom, font, color)
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
        print(self.width, self.height)
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


class Label(Widget):
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
        self.layer = make_text_layer(text, zoom, font, color)
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


class MenuItem: 
    def __init__(
        self, text: str, zoom: int, font, normal_color, selected_color
    ) -> None:
        self.normal = make_text_layer(text, zoom, font, normal_color)
        self.selected = make_text_layer(text, zoom, font, selected_color)
        self.width = self.normal.width

    def draw(self, x: int, y: int, is_selected: bool) -> None:
        (self.selected if is_selected else self.normal).draw(x, y)


class Menu(Widget):
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
        blink_period: float | None = None,
    ) -> None:
        self.items = [
            MenuItem(t, zoom, font, normal_color, selected_color)
            for t in texts
        ]
        self.zoom = zoom
        self.gap = zoom
        self.selected = 0
        n = len(self.items)
        super().__init__(
            max(item.width for item in self.items),
            n * zoom + (n - 1) * self.gap,
            x=x,
            y=y,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            blink_period=blink_period,
        )

    def move(self, delta: int) -> None:
        self.selected = (self.selected + delta) % len(self.items)

    def _render(self) -> None:
        top = self.bottom + self.height
        for i, item in enumerate(self.items):
            item_x = self.left + (self.width - item.width) // 2
            item_y = top - self.zoom - i * (self.zoom + self.gap)
            item.draw(item_x, item_y, i == self.selected)


class HighscoresLabel(Widget):
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
        anchor_y: float = 0.0,
        blink_period: float | None = None,
    ) -> None:
        chars = 3 + 1 + MAX_NAME_LENGTH + 1 + SCORE_DIGITS
        super().__init__(
            chars * zoom,
            MAX_SCORES * zoom,
            x=x,
            y=y,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            blink_period=blink_period,
        )
        self.zoom = zoom
        self.font = font
        self.rank_colors = [top1_color, top2_color, top3_color]
        self.normal_color = normal_color
        self.layer = Layer(self.width, self.height, "RGBA")
        self._drawn: list[tuple[str, int]] | None = None

    def _color_for(self, rank: int, has_score: bool):
        if has_score and rank < len(self.rank_colors):
            return self.rank_colors[rank]
        return self.normal_color

    def set_scores(self, scores: list[tuple[str, int]]) -> None:
        if scores == self._drawn:
            return
        self._drawn = list(scores)
        self.layer.clear()
        for rank in range(MAX_SCORES):
            has_score = rank < len(scores)
            username, score = scores[rank] if has_score else ('-', '-')
            TextRenderer.draw_string(
                self.layer.buffer_view,
                f"{rank + 1:>3}.{username:<{MAX_NAME_LENGTH}} {score}",
                0,
                rank,
                self.zoom,
                self.font,
                self._color_for(rank, has_score),
            )

    def _render(self) -> None:
        self.layer.draw(self.left, self.bottom)


class InputField(Widget):
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

MAX_SCORE_LENGHT = 10

from src.rendering.hud_renderer import format_level, format_time, format_lives, format_score

class Hud(Widget):
    """
    HUD rendering and management
    """    
    def __init__(
        self,
        zoom: int,
        font,
        color,
        *,
        x: int = 0,
        y: int = 0,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0
    ):
        super().__init__(
            30 * zoom,
            2 * zoom,
            x=x,
            y=y,
            anchor_x=anchor_x,
            anchor_y=anchor_y
        )
        self.layer = Layer(self.width, self.height, "RGBA")
        self.zoom, self.font, self.color = zoom, font, color
        self._shown: tuple[str, ...] | None = None

    def set_state(self, game_state) -> None:
        texts = (
            format_time(game_state.level_time_left),
            format_lives(game_state.lives),
            format_level(game_state.level),
            format_score(game_state.score),
        )
        if texts == self._shown:
            return
        self._shown = texts
        self.layer.clear()
        for i, text in enumerate(texts):
            x, y = divmod(i, 2)
            TextRenderer.draw_string(
                self.layer.buffer_view,
                text,
                x * 20,
                y,
                self.zoom,
                self.font,
                self.color,
            )

    def _render(self) -> None:
        self.layer.draw(self.left, self.bottom)
