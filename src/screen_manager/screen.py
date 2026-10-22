from __future__ import annotations
from abc import ABC, abstractmethod
# from enum import Enum
from typing import TYPE_CHECKING
# from pyglet import window, text

if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager


class Screen(ABC):

    def __init__(self, manager: ScreenManager) -> None:
        self.manager = manager

    @abstractmethod
    def input(self, key: int) -> None:
        ...

    def update_screen(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw_screen(self) -> None:
        ...

# class Main(Screen):
#     OPTIONS: list[Screen] = ["Play"]

#     def __init__(self, manager):
#         self.manager: ScreenManager = manager
#         self.selected = 0

#     def input_key(self, key):
#         match key:
#             case window.key.W:
#                 self.selected = (self.selected - 1) % len(self.OPTIONS)
#             case window.key.S:
#                 self.selected = (self.selected + 1) % len(self.OPTIONS)
#             case window.key.ENTER:
#                 self.manager.screens.append(self.OPTIONS[self.selected])

#     def draw_screen(self):
#         label = text.Label(
#             'Main',
#             font_name='Times New Roman',
#             font_size=36,
#             x=window.width//2, y=window.height//2,
#             anchor_x='center', anchor_y='center'
#         )
#         window.clear()
#         label.draw()


# class Play(Screen):
#     OPTIONS: list[Screen] = ["Main"]

#     def __init__(self, manager):
#         self.manager: ScreenManager = manager
#         self.selected = 0

#     def input(self, symbol, modifiers):
#         match symbol:
#             case window.key.W:
#                 self.selected = (self.selected - 1) % len(self.OPTIONS)
#             case window.key.S:
#                 self.selected = (self.selected + 1) % len(self.OPTIONS)
#             case window.key.ENTER:
#                 self.manager.screens.append(self.OPTIONS[self.selected])

#     def draw_screen(self):
#         label = text.Label(
#             'Play',
#             font_name='Times New Roman',
#             font_size=36,
#             x=window.width//2, y=window.height//2,
#             anchor_x='center', anchor_y='center'
#         )
#         window.clear()
#         label.draw()
