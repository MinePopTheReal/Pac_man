from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen
from src.utils.highscore_manager import HighscoreManager, MAX_SCORES, MAX_NAME_LENGTH
from pyglet.window import key as keys

from src.utils.sprite_sheet_manager import Rotation

from src.utils.text_renderer import TextRenderer
from src.rendering.layer import Layer
from src.rendering.assets import Assets, MENU_ZOOM, TITLE_ZOOM, MAJOR_COLOR, MINOR_COLOR, TOP1_COLOR, TOP2_COLOR, TOP3_COLOR, TITLE_MARGIN


TITLE = "HIGHSCORE"

class Highscore(Screen):
    def __init__(self, manager: ScreenManager,
                 highscores: HighscoreManager, assets, config) -> None:
        super().__init__(manager, assets)
        self.highscores = highscores
        self.config = config

        self.title_width = len(TITLE) * TITLE_ZOOM
        self.title_height = TITLE_ZOOM

        self.menu_width = (max((len(str(score)) for _, score in self.highscores.lst_scores), default=0) + MAX_NAME_LENGTH + 3 + len(str(MAX_SCORES))) * MENU_ZOOM
        self.menu_height = MAX_SCORES * MENU_ZOOM

        self.title_layer = Layer(self.title_width, self.title_height, "RGBA")
        self.menu_layer = Layer(self.menu_width, self.menu_height, "RGBA")

        TextRenderer.draw_string(
            self.title_layer.buffer_view,
            TITLE,
            0,
            0,
            TITLE_ZOOM,
            self.assets.font_spritesheet,
            MAJOR_COLOR
        )

    def input(self, key: int) -> None:
        if key in (keys.ESCAPE, keys.ENTER):
            self.manager.pop()

    def draw_screen(self) -> None:
        for rank in range(MAX_SCORES):
            color = MINOR_COLOR
            username, score = '-', '-'
            if rank < len(self.highscores.lst_scores):
                username, score = self.highscores.lst_scores[rank]
                match rank:
                    case 0:
                        color = TOP1_COLOR
                    case 1:
                        color = TOP2_COLOR
                    case 2:
                        color = TOP3_COLOR

            TextRenderer.draw_string(
                self.menu_layer.buffer_view,
                f"{rank + 1:>3}.{username:<{MAX_NAME_LENGTH}} {score}",
                0,
                rank,
                MENU_ZOOM,
                self.assets.font_spritesheet,
                color
            )
        self.title_layer.draw((self.assets.window_width // 2) - (self.title_width // 2), self.assets.window_height - round(self.title_layer.height / TITLE_MARGIN))
        self.menu_layer.draw((self.assets.window_width // 2) - (self.menu_width // 2), (self.assets.window_height // 2) - (self.menu_height // 2))
