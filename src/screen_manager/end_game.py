from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen
from src.utils.highscore_manager import HighscoreManager, MAX_NAME_LENGTH, MAX_SCORES
from pyglet.window import key as keys

from src.utils.text_renderer import TextRenderer
from src.screen_manager.screen import Screen

from src.rendering.layer import Layer
from src.utils.sprite_sheet_manager import Rotation

from src.rendering.assets import Assets, MENU_ZOOM, TITLE_ZOOM, MINOR_COLOR


class EndGame(Screen):
    def __init__(self, manager: ScreenManager, won: bool,
                 manager_highscores: HighscoreManager, score: int, assets) -> None:
        super().__init__(manager, assets)
        self.won = won
        self.manager_highscores = manager_highscores
        self.score = score
        self.name: str = ""

        self.menu_width = MAX_NAME_LENGTH * self.assets.font_spritesheet.spritesheet_config.tile_size * MENU_ZOOM
        self.menu_height = MAX_SCORES * self.assets.font_spritesheet.spritesheet_config.tile_size * MENU_ZOOM
        self.menu_layer = Layer(self.menu_width, self.menu_height, "RGBA")



    def input(self, key: int) -> None:
        if (keys.A <= key <= keys.Z or keys._0 <= key <= keys._9
           or key == keys.SPACE):

            if len(self.name) < MAX_NAME_LENGTH:
                self.name += chr(key).upper()

        elif key == keys.BACKSPACE:
            self.name = self.name[:-1]

        elif key == keys.ENTER:
            self._validate()

        elif key == keys.ESCAPE:
            self.manager.back_to_menu()

    def _validate(self) -> None:
        if not self.manager_highscores.is_valid_name(self.name):
            return
        self.manager_highscores.add_name_score(self.name, self.score)
        self.manager_highscores.save_highscores()
        self.manager.back_to_menu()

    def draw_screen(self) -> None:
        self.menu_layer.clear()
        TextRenderer.draw_string(
            self.menu_layer.buffer_view,
            self.name,
            0,
            0,
            MENU_ZOOM,
            self.assets.font_spritesheet,
            MINOR_COLOR
        )
        self.menu_layer.draw(0, 0)