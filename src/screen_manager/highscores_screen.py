from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen, MENU_ZOOM, TITLE_ZOOM
from src.utils.highscore_manager import HighscoreManager, MAX_SCORES, MAX_NAME_LENGTH
from pyglet.window import key as keys

from src.utils.sprite_sheet_manager import Rotation

from src.utils.text_renderer import TextRenderer
from src.rendering.layer import Layer
TITLE = "HIGHSCORE"

class Highscore(Screen):
    def __init__(self, manager: ScreenManager,
                 highscores: HighscoreManager, assets, config) -> None:
        super().__init__(manager, assets)
        self.highscores = highscores
        self.config = config

        self.highscores.load_highscores()

        self.assets.font_y_spritesheet.preloading_sprites([Rotation.R0], TITLE_ZOOM)

        self.title_width = len(TITLE) * self.assets.font_w_spritesheet.spritesheet_config.tile_size * TITLE_ZOOM
        title_height = self.assets.font_w_spritesheet.spritesheet_config.tile_size * TITLE_ZOOM

        self.menu_width = (max((len(str(score)) for _, score in self.highscores.lst_scores), default=0) + MAX_NAME_LENGTH + 5 + len(str(MAX_SCORES))) * self.assets.font_w_spritesheet.spritesheet_config.tile_size * MENU_ZOOM
        self.menu_height = MAX_SCORES * self.assets.font_w_spritesheet.spritesheet_config.tile_size * MENU_ZOOM

        self.title_layer = Layer(self.title_width, title_height, "RGBA")
        self.menu_layer = Layer(self.menu_width, self.menu_height, "RGBA")

        TextRenderer.draw_string(
            self.title_layer.buffer_view,
            TITLE,
            0,
            0,
            TITLE_ZOOM,
            self.assets.font_y_spritesheet
        )
        self.assets.font_w_spritesheet.preloading_sprites([Rotation.R0], MENU_ZOOM)
        self.assets.font_y_spritesheet.preloading_sprites([Rotation.R0], MENU_ZOOM)

    def input(self, key: int) -> None:
        if key in (keys.ESCAPE, keys.ENTER):
            self.manager.pop()

    def draw_screen(self) -> None:
        for i, (score, username) in enumerate(self.highscores.lst_scores):
            TextRenderer.draw_string(
                self.menu_layer.buffer_view,
                f"{i}. {username} ({score})",
                0,
                i,
                MENU_ZOOM,
                self.assets.font_w_spritesheet
            )
        self.title_layer.draw((self.assets.screen_width // 2) - (self.title_width // 2), (self.assets.window_height + (self.assets.screen_height // 2) - (self.menu_height // 2)) // 2)
        self.menu_layer.draw((self.assets.screen_width // 2) - (self.menu_width // 2), (self.assets.screen_height // 2) - (self.menu_height // 2))
