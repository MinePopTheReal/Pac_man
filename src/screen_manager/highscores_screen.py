from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.utils.widget.highscores_label import HighscoresLabel
from src.utils.highscore_manager import HighscoreManager
from src.rendering.display import SCALE_FACTOR
from src.screen_manager.screen import Screen
from src.parsing.models import GameConfig
from src.utils.widget.label import Label
from src.rendering.assets import Assets
from src.rendering.assets import (
    H1_PX_SIZE, 
    H3_PX_SIZE, 
    MAJOR_COLOR, 
    MINOR_COLOR, 
    TOP1_COLOR, 
    TOP2_COLOR, 
    TOP3_COLOR
)

from pyglet.window import key as keys


class Highscore(Screen):
    TITLE = "HIGHSCORE"

    def __init__(
        self,
        manager: ScreenManager,
        highscores: HighscoreManager,
        assets: Assets,
        config: GameConfig
    ) -> None:
        super().__init__(manager, assets)
        self.highscores = highscores
        self.config = config

        self.title = Label(
            self.TITLE,
            H1_PX_SIZE,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=self.assets.window_height - 200 * SCALE_FACTOR,
            anchor_x=0.5,
            anchor_y=1
        )

        title_bottom = self.title.y - self.title.height
        self.highscores_label = HighscoresLabel(
            H3_PX_SIZE,
            self.assets.font_spritesheet,
            TOP1_COLOR,
            TOP2_COLOR,
            TOP3_COLOR,
            MINOR_COLOR,
            x=self.assets.window_width // 2,
            y=title_bottom - 200 * SCALE_FACTOR,
            anchor_x=0.5,
            anchor_y=1
        )

    def input(self, key: int) -> None:
        if key in (keys.ESCAPE, keys.ENTER):
            self.manager.pop()

    def draw_screen(self) -> None:
        self.title.draw()
        self.highscores_label.set_scores(self.highscores.lst_scores)
        self.highscores_label.draw()