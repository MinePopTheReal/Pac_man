from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen
from enum import Enum
from src.game_state.game_state import GameState
from pyglet.window import key as keys
from pyglet import text


class PauseOption(Enum):
    RESUME = 'Resume'
    MENU = 'Back to menu'


class Pause(Screen):
    def __init__(self, manager: ScreenManager, game: GameState, assets):
        super().__init__(manager, assets)
        self.game = game
        self.selected: int = 0
        self.options: list[PauseOption] = list(PauseOption)

    def input(self, key: int) -> None:
        match key:
            case keys.W | keys.UP:
                self.selected = (self.selected - 1) % len(self.options)
            case keys.S | keys.DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            case keys.ENTER:
                self._validate(self.options[self.selected])
            case keys.ESCAPE:
                self._validate(PauseOption.RESUME)

    def _validate(self, option: PauseOption) -> None:
        match option:
            case PauseOption.RESUME:
                self.game.switch_pause()
                self.manager.pop()
            case PauseOption.MENU:
                self.manager.back_to_menu()

    def draw_screen(self) -> None:
        label = text.Label(
                f"Pause",
                font_name="Arial",
                font_size=32,
                x=self.assets.window_width // 2,
                y=(self.assets.window_height // 2) + 45,
                anchor_x="center",
                anchor_y="center",
                color=(255, 0, 255, 255),
            )
        label.draw()
        for i in range(len(self.options)):
            if i == self.selected:
                color = (255, 255, 0, 255)
            else:
                color = (255, 255, 255, 255)
            label = text.Label(
                f"{self.options[i]}",
                font_name="Arial",
                font_size=32,
                x=self.assets.window_width // 2,
                y=(self.assets.window_height // 2) - i * 45,
                anchor_x="center",
                anchor_y="center",
                color=color,
            )
            label.draw()
