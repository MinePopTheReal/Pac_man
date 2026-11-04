from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.rendering.assets import Assets, H3_PX_SIZE, H1_PX_SIZE, MAJOR_COLOR, MINOR_COLOR
from src.screen_manager.instructions_screen import Instructions
from src.screen_manager.highscores_screen import Highscore
from src.utils.highscore_manager import HighscoreManager
from src.screen_manager.game_screen import Play
from src.rendering.display import SCALE_FACTOR
from src.screen_manager.screen import Screen
from src.parsing.models import GameConfig
from src.utils.widget.label import Label
from src.utils.widget.menu import Menu


from pyglet.window import key as keys
from enum import Enum

class Options(Enum):
    START = 'Start'
    HIGHSCORES = 'Scores'
    INSTRUCTIONS = 'Rules'
    EXIT = 'Quit'


class MainMenu(Screen):
    TITLE = "PAC-MAN"

    def __init__(self, config: GameConfig, manager: ScreenManager, assets: Assets, highscores: HighscoreManager) -> None:
        super().__init__(manager, assets)
        self.config = config
        self.options: list[Options] = list(Options)
        self.selected: int = 0
        self.highscores = highscores

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
        self.menu = Menu(
            [option.value for option in self.options],
            H3_PX_SIZE,
            self.assets.font_spritesheet,
            MINOR_COLOR,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=title_bottom - 800 * SCALE_FACTOR,
            anchor_x=0.5,
            anchor_y=0
        )

        menu_bottom = self.menu.y - self.menu.height
        self.helper_text = Label(
            "press enter",
            H3_PX_SIZE,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=menu_bottom + 200 * SCALE_FACTOR,
            anchor_x=0.5,
            anchor_y=1,
            blink_period=0.2
        )

    def update_screen(self, dt: float) -> None:
        self.helper_text.update(dt)

    def input(self, key: int) -> None:
        match key:
            case keys.W | keys.UP:
                self.menu.move(-1)
            case keys.S | keys.DOWN:
                self.menu.move(1)
            case keys.ENTER:
                self._validate(self.menu.selected)
            case keys.ESCAPE:
                self.manager.quit()

    # TODO Change this so that an instance isn't created every time
    def _validate(self, selected: int) -> None:
        match self.options[selected]:
            case Options.START:
                self.manager.push(Play(self.config, self.manager, self.assets, self.highscores))
            case Options.HIGHSCORES:
                self.manager.push(Highscore(self.manager, self.highscores, self.assets, self.config))
            case Options.INSTRUCTIONS:
                self.manager.push(Instructions(self.manager, self.assets))
            case Options.EXIT:
                self.manager.quit()

    def draw_screen(self) -> None:
        self.menu.draw()
        self.title.draw()
        self.helper_text.draw()
