from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen
from enum import Enum
from src.parsing.models import GameConfig
from pyglet.window import key as keys
from src.screen_manager.game_screen import Play
from src.screen_manager.instructions_screen import Instructions
from src.utils.highscore_manager import HighscoreManager
from src.screen_manager.highscores_screen import Highscore

from src.rendering.display import Display
from src.utils.widget import Label



from pyglet import text

from src.utils.text_renderer import TextRenderer
from src.rendering.layer import Layer
from src.utils.sprite_sheet_manager import Rotation
from src.rendering.assets import Assets, MENU_ZOOM, TITLE_ZOOM, MAJOR_COLOR, MINOR_COLOR, TITLE_MARGIN, ENTITIES_SIZE

class Options(Enum):
    START = 'Start'
    HIGHSCORES = 'Scores'
    INSTRUCTIONS = 'Rules'
    EXIT = 'Quit'

TITLE = "PAC-MAN"

class MainMenu(Screen):
    def __init__(self, config: GameConfig, manager: ScreenManager, assets, highscores: HighscoreManager) -> None:
        super().__init__(manager, assets)
        self.config = config
        self.options: list[Options] = list(Options)
        self.selected: int = 0
        self.highscores = highscores

        self.title_width = len(TITLE) * TITLE_ZOOM
        self.title_height = TITLE_ZOOM

        self.menu_width = len(max(self.options, key=lambda x: len(x.value)).value) * MENU_ZOOM
        self.menu_height = (len(self.options) * 2) * MENU_ZOOM

        self.title = Label(
            TITLE,
            TITLE_ZOOM,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=self.assets.window_height - 100,
            anchor_x=0.5,
            anchor_y=1
            )

        # self.title_layer = Layer(self.title_width, self.title_height, "RGBA")
        # self.menu_layer = Layer(self.menu_width, self.menu_height, "RGBA")

        # TextRenderer.draw_string(
        #     self.title_layer.buffer_view,
        #     TITLE,
        #     0,
        #     0,
        #     TITLE_ZOOM,
        #     self.assets.font_spritesheet,
        #     MAJOR_COLOR
        # )

    def input(self, key: int) -> None:
        match key:
            case keys.W | keys.UP:
                self.selected = (self.selected - 1) % len(self.options)
            case keys.S | keys.DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            case keys.ENTER:
                self._validate(self.options[self.selected])

    # TODO Change this so that an instance isn't created every time 
    def _validate(self, option: Options) -> None:
        match option:
            case Options.START:
                self.manager.push(Play(self.config, self.manager, self.assets, self.highscores))
            case Options.HIGHSCORES:
                self.manager.push(Highscore(self.manager, self.highscores, self.assets, self.config))
            case Options.INSTRUCTIONS:
                self.manager.push(Instructions(self.manager, self.assets))
            case Options.EXIT:
                self.manager.quit()

    def draw_screen(self) -> None:
        # for i in range(len(self.options)):
            # TextRenderer.draw_string(
            #     self.menu_layer.buffer_view,
            #     self.options[i].value,
            #     0,
            #     i * 2,
            #     MENU_ZOOM,
            #     self.assets.font_spritesheet,
            #     MAJOR_COLOR if i == self.selected else MINOR_COLOR
            # )
        # self.title_layer.draw()
        self.title.draw()
        # self.menu_layer.draw((self.assets.window_width // 2) - (self.menu_width // 2), (self.assets.window_height // 2) - (self.menu_height // 2))
