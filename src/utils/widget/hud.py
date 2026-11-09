from src.utils.sprite_sheet_manager import SpriteSheetManager
from src.utils.text_renderer import draw_string
from src.game_state.game_state import MAX_SCORE
from src.game_state.game_state import GameState
from src.utils.widget.widget import Widget
from src.rendering.layer import Layer


from collections.abc import Callable
from math import ceil


def format_time(seconds: float) -> str:
    """Format the time left in the level as "time: minutes:seconds".

    The seconds are rounded down, and the minutes are not limited to 59.

    Args:
        seconds (float): The time left, in seconds.

    Returns:
        str: The text of the line, for example "time: 1:05".
    """
    minutes, secs = divmod(int(seconds), 60)
    return f"{"time":>5}: {minutes}:{secs:02d}"


def format_lives(lives: int) -> str:
    """Format the lives left as hearts.

    At most 3 hearts are shown. If there are more lives, a "+" is added
    after the hearts.

    Args:
        lives (int): The number of lives left.

    Returns:
        str: The text of the line, for example "lives: ❤❤❤+".
    """
    return f"{"lives":>5}: " + "❤" * min(lives, 3) + ("+" if lives > 3 else "")


def format_level(level: int) -> str:
    """Format the number of the current level.

    Args:
        level (int): The number of the level.

    Returns:
        str: The text of the line, for example "level: 3".
    """
    return f"{"level":>5}: " + str(level)


def format_score(score: int) -> str:
    """Format the score of the player.

    Args:
        score (int): The current score.

    Returns:
        str: The text of the line, for example "score: 1200".
    """
    return f"{"score":>5}: " + str(score)


def format_cheat(active: bool) -> str:
    """Format the cheat mode indicator.

    When the cheat mode is off, the text is made of spaces of the same
    length, so it erases the indicator and the layout does not move.

    Args:
        active (bool): True if the cheat mode is on.

    Returns:
        str: "cheat: ON", or the same number of spaces.
    """
    text = "cheat: ON"
    return text if active else " " * len(text)


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
    Widget that shows the information of the game above the maze.

    It shows the time left, the lives, the level, the score and the
    cheat indicator, in a grid of INFO_PER_LINE columns. The texts are
    drawn into their own layer, which is redrawn only when one of them
    changes.
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
        """Update the texts with the current state of the game.

        Does nothing if the texts are the same as the last time, so it
        can be called every frame at no cost.

        Args:
            game_state (GameState): The game to read the time, the lives,
                the level, the score and the cheat mode from.
        """
        texts = [line(game_state) for line in HUD_LINES]

        if texts == self._shown:
            return
        self._shown = texts
        self.layer.clear()
        for i, text in enumerate(texts):
            y, x = divmod(i, INFO_PER_LINE)

            draw_string(
                self.layer.buffer_view,
                text,
                x * self.column_width,
                y,
                self.zoom,
                self.font,
                self.color,
            )

    def _render(self) -> None:
        """Put the layer of the HUD in the window."""
        self.layer.draw(self.left, self.bottom)
