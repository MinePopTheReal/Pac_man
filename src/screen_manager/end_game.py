from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen
from src.utils.highscore_manager import HighscoreManager, MAX_NAME_LENGTH, MAX_SCORES
from pyglet.window import key as keys

from src.utils.text_renderer import TextRenderer
from src.screen_manager.screen import Screen

from src.rendering.layer import Layer
from src.utils.sprite_sheet_manager import Rotation

from src.rendering.assets import Assets, MENU_ZOOM, TITLE_ZOOM, MINOR_COLOR, MAJOR_COLOR
from src.utils.widget import InputField, Label
from src.rendering.display import SCALE_FACTOR

SCORE_MARGIN = MENU_ZOOM * 2

class EndGame(Screen):
    def __init__(self, manager: ScreenManager, won: bool,
                 manager_highscores: HighscoreManager, score: int, assets) -> None:
        super().__init__(manager, assets)
        self.won = won
        self.manager_highscores = manager_highscores
        self.score = score

        self.prompt = "Enter your username:"
        self.name: str = ""
        self.empty: str = "_" * MAX_NAME_LENGTH
        self.title = Label(
            "you win" if won else "you lose",
            TITLE_ZOOM, self.assets.font_spritesheet, MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=self.assets.window_height - 200 * SCALE_FACTOR,
            anchor_x=0.5, anchor_y=1,
        )

        title_bottom = self.title.y - self.title.height
        self.score_label = Label(
            f"your score: {self.score}",
            MENU_ZOOM, self.assets.font_spritesheet, MINOR_COLOR,
            x=self.assets.window_width // 2,
            y=title_bottom - SCORE_MARGIN,
            anchor_x=0.5, anchor_y=1,
        )

        score_bottom = self.score_label.y - self.score_label.height
        self.input_field = InputField(
            self.prompt,
            MENU_ZOOM, self.assets.font_spritesheet, MAJOR_COLOR, MINOR_COLOR,
            x=self.assets.window_width // 2,
            y=score_bottom // 2,
            anchor_x=0.5, anchor_y=0.5,
        )

    def input(self, key: int) -> None:
        if (keys.A <= key <= keys.Z or keys._0 <= key <= keys._9
           or key == keys.SPACE):

            if len(self.name) < MAX_NAME_LENGTH:
                self.name += chr(key).upper()
                self.empty = self.empty[:-1]

        elif key == keys.BACKSPACE:
            self.name = self.name[:-1]
            if len(self.empty) < MAX_NAME_LENGTH:
                self.empty += "_"

        elif key == keys.ENTER:
            self._validate()

        elif key == keys.ESCAPE:
            self.manager.back_to_menu()

    def _validate(self) -> None:
        if not self.manager_highscores.is_valid_name(self.name):
            return
        self.manager_highscores.add_name_score(self.name, self.score)
        self.manager_highscores.save_highscores()
        self.manager.back_to_menu()

    def draw_screen(self) -> None:
        self.title.draw()
        self.score_label.draw()
        self.input_field.draw((' ' * ((len(self.prompt) // 2) - MAX_NAME_LENGTH // 2))+ self.name + self.empty)
