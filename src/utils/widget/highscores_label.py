from src.game_state.game_state import MAX_SCORE_DIGITS
from src.utils.widget.input_field import MAX_NAME_LENGTH
from src.utils.highscore_manager import MAX_HIGHSCORE
from src.utils.text_renderer import TextRenderer
from src.utils.widget.widget import Widget
from src.rendering.layer import Layer

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
        chars = 3 + 1 + MAX_NAME_LENGTH + 1 + MAX_SCORE_DIGITS
        super().__init__(
            chars * zoom,
            MAX_HIGHSCORE * zoom,
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
        for rank in range(MAX_HIGHSCORE):
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
