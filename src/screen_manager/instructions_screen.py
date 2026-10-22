from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen
from pyglet.window import key as keys


class Instructions(Screen):
    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)

    def input(self, key: int) -> None:
        if key in (keys.ESCAPE, keys.ENTER):
            self.manager.pop()

    def draw_screen(self) -> None:
        ...
