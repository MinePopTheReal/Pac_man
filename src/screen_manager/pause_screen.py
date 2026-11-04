from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.rendering.assets import H1_PX_SIZE, H3_PX_SIZE, MAJOR_COLOR, MINOR_COLOR, SCALE_FACTOR
from src.game_state.game_state import GameState
from src.screen_manager.screen import Screen
from src.utils.widget.label import Label
from src.utils.widget.menu import Menu

from pyglet.window import key as keys
from enum import Enum


class PauseOption(Enum):
    RESUME = 'Resume'
    MENU = 'Back to menu'


class Pause(Screen):
    TITLE = "pause"

    def __init__(self, manager: ScreenManager, game: GameState, assets):
        super().__init__(manager, assets)
        self.game = game
        self.selected: int = 0
        self.options: list[PauseOption] = list(PauseOption)

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

    def input(self, key: int) -> None:
        match key:
            case keys.W | keys.UP:
                self.menu.move(1)
            case keys.S | keys.DOWN:
                self.menu.move(-1)
            case keys.ENTER:
                self._validate(self.menu.selected)
            case keys.ESCAPE:
                self._validate(0)

    def _validate(self, selected: int = 0) -> None:
        match self.options[selected]:
            case PauseOption.RESUME:
                self.game.switch_pause()
                self.manager.pop()
            case PauseOption.MENU:
                self.manager.back_to_menu()

    def draw_screen(self) -> None:
        self.title.draw()
        self.menu.draw()
