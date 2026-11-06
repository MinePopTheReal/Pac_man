from src.utils.sprite_sheet_manager import SpriteSheetManager
from src.utils.text_renderer import TextRenderer
from src.game_state.game_state import MAX_SCORE
from src.game_state.game_state import GameState
from src.utils.widget.widget import Widget
from src.rendering.layer import Layer


from collections.abc import Callable
from math import ceil


def format_time(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    return f"{"time":>5}: {minutes}:{secs:02d}"


def format_lives(lives: int) -> str:
    return f"{"lives":>5}: " + "❤" * min(lives, 3) + ("+" if lives > 3 else "")


def format_level(level: int) -> str:
    return f"{"level":>5}: " + str(level)


def format_score(score: int) -> str:
    return f"{"score":>5}: " + str(score)


def format_cheat(active: bool) -> str:
    text = "cheat: ON"
    return text if active else "" * len(text)


HudLine = Callable[[GameState], str]

HUD_LINES: tuple[HudLine, ...] = (
    lambda s: format_time(s.level_time_left),
    lambda s: format_lives(s.lives),
    lambda s: format_level(s.level),
    lambda s: format_score(s.score),
    lambda s: format_cheat(s.cheats.enabled),
)

LONGEST_TEXTS = (
    format_time(99 * 60 + 59),   # "time: 99:59"
    format_lives(4),             # 3 hearts + "+"
    format_level(99),
    format_score(MAX_SCORE),
    format_cheat(True),
)

INFO_PER_LINE = 2
LINE_NUMBER = ceil(len(LONGEST_TEXTS) / INFO_PER_LINE)
COLUMN_GAP = 1


class Hud(Widget):
    """
    HUD rendering and management
    """
    def __init__(
        self,
        zoom: int,
        font: SpriteSheetManager,
        color: tuple[int, int, int],
        *,
        x: int = 0,
        y: int = 0,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0
    ) -> None:
        self.column_width = max(len(t) for t in LONGEST_TEXTS) + COLUMN_GAP
        super().__init__(
            INFO_PER_LINE * self.column_width * zoom,
            LINE_NUMBER * zoom,
            x=x,
            y=y,
            anchor_x=anchor_x,
            anchor_y=anchor_y
        )
        self.layer = Layer(self.width, self.height, "RGBA")
        self.zoom, self.font, self.color = zoom, font, color
        self._shown: list[str] | None = None

    def set_state(self, game_state: GameState) -> None:
        texts = [line(game_state) for line in HUD_LINES]

        if texts == self._shown:
            return
        self._shown = texts
        self.layer.clear()
        for i, text in enumerate(texts):
            y, x = divmod(i, INFO_PER_LINE)

            TextRenderer.draw_string(
                self.layer.buffer_view,
                text,
                x * self.column_width,
                y,
                self.zoom,
                self.font,
                self.color,
            )

    def _render(self) -> None:
        self.layer.draw(self.left, self.bottom)
