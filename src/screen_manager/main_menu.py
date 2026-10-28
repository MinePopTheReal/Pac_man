from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen, MENU_ZOOM, TITLE_ZOOM
from enum import Enum
from src.parsing.models import GameConfig
from pyglet.window import key as keys
from src.screen_manager.game_screen import Play
from src.screen_manager.instructions_screen import Instructions
from src.utils.highscore_manager import HighscoreManager
from src.screen_manager.highscores_screen import Highscore
from src.screen_manager.instructions_screen import Instructions

from src.rendering.display import Display
from pyglet import text

from src.utils.text_renderer import TextRenderer
from src.rendering.layer import Layer
from src.utils.sprite_sheet_manager import Rotation


class Options(Enum):
    START = 'Start'
    HIGHSCORES = 'Scores'
    INSTRUCTIONS = 'Rules'
    EXIT = 'Quit'


TITLE = "PACMAN"


class MainMenu(Screen):
    def __init__(self,manager: ScreenManager, config: GameConfig, assets,
                 highscores: HighscoreManager,
                 instructions_screen: Instructions, play_screen: Play,
                 highscores_screen: Highscore) -> None:
        super().__init__(manager, assets)
        self.config = config
        self.options: list[Options] = list(Options)
        self.selected: int = 0
        self.highscores = highscores
        self.instructions_screen = instructions_screen
        self.play_screen = play_screen
        self.highscores_screen = highscores_screen

        self.assets.font_y_spritesheet.preloading_sprites([Rotation.R0], TITLE_ZOOM)

        self.title_width = len(TITLE) * self.assets.font_w_spritesheet.spritesheet_config.tile_size * TITLE_ZOOM
        title_height = self.assets.font_w_spritesheet.spritesheet_config.tile_size * TITLE_ZOOM

        self.menu_width = len(max(self.options, key=lambda x: len(x.value)).value) * self.assets.font_w_spritesheet.spritesheet_config.tile_size * MENU_ZOOM
        self.menu_height = len(self.options) * self.assets.font_w_spritesheet.spritesheet_config.tile_size * MENU_ZOOM

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
        match key:
            case keys.W | keys.UP:
                self.selected = (self.selected - 1) % len(self.options)
            case keys.S | keys.DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            case keys.ENTER:
                self._validate(self.options[self.selected])

    # TODO Change this so that an instance isn't created every times
    def _validate(self, option: Options) -> None:
        match option:
            case Options.START:
                self.manager.push(self.play_screen)
            case Options.HIGHSCORES:
                self.manager.push(self.highscores_screen)
            case Options.INSTRUCTIONS:
                self.manager.push(self.instructions_screen)
            case Options.EXIT:
                self.manager.quit()

    def reset(self) -> None:
        self.selected = 0

    def draw_screen(self) -> None:

        for i in range(len(self.options)):
            if i == self.selected:
                sprite_sheet = self.assets.font_y_spritesheet
            else:
                sprite_sheet = self.assets.font_w_spritesheet
            TextRenderer.draw_string(
                self.menu_layer.buffer_view,
                self.options[i].value,
                0,
                i,
                MENU_ZOOM,
                sprite_sheet
            )
        self.title_layer.draw((self.assets.screen_width // 2) - (self.title_width // 2), (self.assets.window_height + (self.assets.screen_height // 2) - (self.menu_height // 2)) // 2)
        self.menu_layer.draw((self.assets.screen_width // 2) - (self.menu_width // 2), (self.assets.screen_height // 2) - (self.menu_height // 2))
