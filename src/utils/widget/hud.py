from src.utils.text_renderer import TextRenderer
from src.game_state.game_state import MAX_SCORE
from src.game_state.game_state import GameState
from src.utils.widget.widget import Widget 
from src.rendering.layer import Layer

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


MAXIMUM_VALUE = (
    99 * 60 + 59,      # "time: 99:59"
    4,                 # 3 hearts + "+"
    99,                # level max
    MAX_SCORE,          # score at its cap
    11
)

FORMATERS = (
    format_time,
    format_lives,
    format_level,
    format_score,
    format_cheat
)

INFO_PER_LINE = 2
LINE_NUMBER = ceil(len(FORMATERS) / INFO_PER_LINE)
COLUMN_GAP = 1

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
        self.column_width = max(len(f(v)) for f, v in zip(FORMATERS, MAXIMUM_VALUE)) + COLUMN_GAP
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
        attribute_to_consider = (
            lambda: game_state.level_time_left,
            lambda: game_state.lives,
            lambda: game_state.level,
            lambda: game_state.score,
            lambda: game_state.cheats.enabled
        )
        texts = [f(v()) for f, v in zip(FORMATERS, attribute_to_consider)]

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
