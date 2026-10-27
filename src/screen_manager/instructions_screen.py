from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen
from pyglet.window import key as keys

from pyglet import text
class Instructions(Screen):
    def __init__(self, manager: ScreenManager, assets) -> None:
        super().__init__(manager, assets)


    def input(self, key: int) -> None:
        if key in (keys.ESCAPE, keys.ENTER):
            self.manager.pop()

    def draw_screen(self) -> None:
        label = text.Label(
                f"Instructions",
                font_name="Arial",
                font_size=32,
                x=self.assets.window_width // 2,
                y=(self.assets.window_height // 2) + 45,
                anchor_x="center",
                anchor_y="center",
                color=(255, 0, 255, 255),
            )
        label.draw()
        # for i in range(len(self.options)):
        #     if i == self.selected:
        #         color = (255, 255, 0, 255)
        #     else:
        #         color = (255, 255, 255, 255)
        #     label = text.Label(
        #         f"{self.options[i]}",
        #         font_name="Arial",
        #         font_size=32,
        #         x=self.assets.window_width // 2,
        #         y=(self.assets.window_height // 2) - i * 45,
        #         anchor_x="center",
        #         anchor_y="center",
        #         color=color,
        #     )
        #     label.draw()


