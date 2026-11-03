from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen
from pyglet.window import key as keys

from src.utils.widget import Label
from src.rendering.assets import H1_PX_SIZE, SCALE_FACTOR, MAJOR_COLOR, H3_PX_SIZE, MINOR_COLOR, H1_PX_SIZE, H3_PX_SIZE, H5_PX_SIZE

TITLE = "RULES"

class Instructions(Screen):
    def __init__(self, manager: ScreenManager, assets) -> None:
        super().__init__(manager, assets)
        self.rules: str = (
            "EAT ALL THE PACGUMS TO\n"
            "CLEAR THE LEVEL.\n\n"
            "AVOID THE 4 GHOSTS.\n"
            "IF ONE TOUCHES YOU\n"
            "YOU LOSE A LIFE.\n\n"
            "SUPER PACGUMS MAKE GHOSTS\n"
            "VULNERABLE FOR A FEW SECONDS\n"
            "EAT THEM FOR BONUS POINTS.\n\n"
            "NO LIVES LEFT:\n"
            "GAME OVER\n\n"
            "GET THE BEST SCORE.\n"
        )
        
        self.title = Label(
            TITLE,
            H1_PX_SIZE,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=self.assets.window_height - 200 * SCALE_FACTOR,
            anchor_x=0.5,
            anchor_y=1
        )

        title_bottom = self.title.y - self.title.height
        self.rules_label = Label(
            self.rules,
            H5_PX_SIZE,
            self.assets.font_spritesheet,
            MINOR_COLOR,
            x=self.assets.window_width // 2,
            y=title_bottom - 200 * SCALE_FACTOR,
            anchor_x=0.5,
            anchor_y=1
        )

    def input(self, key: int) -> None:
        if key in (keys.ESCAPE, keys.ENTER):
            self.manager.pop()

    def draw_screen(self) -> None:
        self.title.draw()
        self.rules_label.draw()