from src.rendering.sprite_sheet_manager import SpriteSheetManager
from src.rendering.widget.input_field import MAX_NAME_LENGTH
from src.game_state.game_state import MAX_SCORE_DIGITS
from src.utils.high_score_manager import MAX_HIGH_SCORE
from src.rendering.text_drawing import draw_string
from src.rendering.widget.widget import Widget
from src.rendering.layer import Layer


class HighScoreLabel(Widget):
    """Widget that draws the list of the best scores.

    Each line shows the rank, the name and the score. The list always has
    MAX_HIGH_SCORE lines: the missing scores are shown as "-". The first
    three lines each have their own color. The list is drawn into its own
    layer, which is redrawn only when the scores change.
    """
    def __init__(
        self,
        zoom: int,
        font: SpriteSheetManager,
        top1_color: tuple[int, int, int],
        top2_color: tuple[int, int, int],
        top3_color: tuple[int, int, int],
        normal_color: tuple[int, int, int],
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
            MAX_HIGH_SCORE * zoom,
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

    def _color_for(
        self,
        rank: int,
        has_score: bool
    ) -> tuple[int, int, int]:
        """Give the color of a line of the list.

        Args:
            rank (int): The position of the line, starting at 0.
            has_score (bool): True if the line shows a real score, False
                if it is an empty line.

        Returns:
            tuple[int, int, int]: The color of the line: the color of its
                rank for the first three real scores, else the normal
                color.
        """
        if has_score and rank < len(self.rank_colors):

            return self.rank_colors[rank]
        return self.normal_color

    def set_scores(self, scores: list[tuple[str, int]]) -> None:
        """Draw the list of scores in the layer.

        Does nothing if the scores are the same as the last time, so the
        layer is not redrawn every frame. The name and the score of each
        line must fit in the space planned for them (MAX_NAME_LENGTH
        characters and MAX_SCORE_DIGITS digits).

        Args:
            scores (list[tuple[str, int]]): The (name, score) pairs, from
                the best to the worst.
        """
        if scores == self._drawn:
            return
        self._drawn = list(scores)
        self.layer.clear()
        for rank in range(MAX_HIGH_SCORE):
            has_score = rank < len(scores)
            username, score = scores[rank] if has_score else ("-", "-")
            draw_string(
                self.layer.buffer_view,
                f"{rank + 1:>3}.{username:<{MAX_NAME_LENGTH}} {score}",
                0,
                rank,
                self.zoom,
                self.font,
                self._color_for(rank, has_score),
            )

    def _render(self) -> None:
        """Put the layer of the list in the window."""
        self.layer.draw(self.left, self.bottom)
