from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen
from enum import Enum
from src.parsing.models import GameConfig
from pyglet.window import key as keys
from src.screen_manager.game_screen import Play


class Options(Enum):
    START = 'Start Game'
    HIGHSCORES = 'Scores'
    INSTRUCTIONS = 'Rules'
    EXIT = 'Quit'


class MainMenu(Screen):
    def __init__(self, config: GameConfig, manager: ScreenManager) -> None:
        super().__init__(manager)
        self.config = config
        self.options: list[Options] = list(Options)
        self.selected: int = 0

    def input(self, key: int) -> None:
        match key:
            case keys.W | keys.UP:
                self.selected = (self.selected - 1) % len(self.options)
            case keys.S | keys.DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            case keys.ENTER:
                self._validate(self.options[self.selected])

    def _validate(self, option: Options) -> None:
        match option:
            case Options.START:
                self.manager.push(Play(self.config, self.manager))
            case Options.HIGHSCORES:
                ...
            case Options.INSTRUCTIONS:
                ...
            case Options.EXIT:
                self.manager.quit()

    def draw_screen(self) -> None:
        ...
