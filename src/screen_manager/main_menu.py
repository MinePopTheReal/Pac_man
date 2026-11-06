from src.screen_manager.screen_manager import ScreenName
from src.screen_manager.screen import Screen, Navigator
from src.parsing.models import GameConfig
from src.utils.widget.label import Label
from src.utils.widget.menu import Menu
from src.rendering.assets import (
    Assets,
    H3_PX_SIZE,
    H1_PX_SIZE,
    MAJOR_COLOR,
    MINOR_COLOR,
    SCALE_FACTOR
)


from pyglet.window import key as keys
from enum import Enum


class Options(Enum):
    START = 'Start'
    HIGHSCORES = 'Scores'
    INSTRUCTIONS = 'Rules'
    EXIT = 'Quit'


class MainMenu(Screen):
    TITLE = "PAC-MAN"

    def __init__(
        self,
        config: GameConfig,
        navigator: Navigator,
        assets: Assets
    ) -> None:
        super().__init__(navigator, assets)
        self.config = config
        self.options: list[Options] = list(Options)

        self.set_screens()

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
                self.navigator.quit()

    def set_screens(self) -> None:
        self.selected: int = 0

        self.title = Label(
            self.TITLE,
            H1_PX_SIZE,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(self.assets.window_height - 200 * SCALE_FACTOR),
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
            y=int(title_bottom - 800 * SCALE_FACTOR),
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
            y=int(menu_bottom + 200 * SCALE_FACTOR),
            anchor_x=0.5,
            anchor_y=1,
            blink_period=0.2
        )

    def _validate(self, selected: int) -> None:
        match self.options[selected]:
            case Options.START:
                self.navigator.push(ScreenName.PLAY)
            case Options.HIGHSCORES:
                self.navigator.push(ScreenName.HIGHSCORE)
            case Options.INSTRUCTIONS:
                self.navigator.push(ScreenName.INSTRUCTION)
            case Options.EXIT:
                self.navigator.quit()

    def draw_screen(self) -> None:
        self.menu.draw()
        self.title.draw()
        self.helper_text.draw()
