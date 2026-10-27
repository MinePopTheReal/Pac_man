from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen
from src.utils.highscore_manager import HighscoreManager, MAX_NAME_LENGTH
from pyglet.window import key as keys


class EndGame(Screen):
    def __init__(self, manager: ScreenManager, won: bool,
                 manager_highscores: HighscoreManager, score: int) -> None:
        super().__init__(manager)
        self.won = won
        self.manager_highscores = manager_highscores
        self.score = score
        self.name: str = ""

    def input(self, key: int) -> None:
        if (keys.A <= key <= keys.Z or keys._0 <= key <= keys._9
           or key == keys.SPACE):

            if len(self.name) < MAX_NAME_LENGTH:
                self.name += chr(key).upper()

        elif key == keys.BACKSPACE:
            self.name = self.name[:-1]

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
        ...
