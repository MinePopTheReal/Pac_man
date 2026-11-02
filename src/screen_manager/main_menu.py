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
from src.utils.widget import Label, Menu



from pyglet import text

from src.utils.text_renderer import TextRenderer
from src.rendering.layer import Layer
from src.utils.sprite_sheet_manager import Rotation
from src.rendering.assets import Assets, MENU_ZOOM, TITLE_ZOOM, MAJOR_COLOR, MINOR_COLOR, TITLE_MARGIN, ENTITIES_SIZE
from src.rendering.display import SCALE_FACTOR

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

        self.title = Label(
            TITLE,
            TITLE_ZOOM,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=self.assets.window_height - 200 * SCALE_FACTOR,
            anchor_x=0.5,
            anchor_y=1
        )
        self.menu = Menu(
            [option.value for option in self.options],
            MENU_ZOOM,
            self.assets.font_spritesheet,
            MINOR_COLOR,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=(self.title.y - TITLE_ZOOM) // 2,
            anchor_x=0.5,
            anchor_y=0.4
        )
        self.helper_text = Label(
            "press enter",
            MENU_ZOOM,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=(((self.title.y - TITLE_ZOOM) // 2) - self.menu.height) // 2,
            anchor_x=0.5,
            anchor_y=0,
            blink_period=0.15
        )

    def update_screen(self, dt: float) -> None:
        self.helper_text.update(dt)
        
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
        self.menu.draw(self.selected)
        self.title.draw()
        self.helper_text.draw()
