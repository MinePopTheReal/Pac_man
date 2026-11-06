from src.rendering.assets import (
    Assets,
    H1_PX_SIZE,
    H3_PX_SIZE,
    MAJOR_COLOR,
    MINOR_COLOR,
    SCALE_FACTOR
)
from src.screen_manager.screen import Screen, Navigator
from src.game_state.session import Session
from src.utils.widget.label import Label
from src.utils.widget.menu import Menu


from pyglet.window import key as keys
from enum import Enum


class PauseOption(Enum):
    RESUME = 'Resume'
    MENU = 'Back to menu'


class Pause(Screen):
    TITLE = "pause"

    def __init__(self, navigator: Navigator, session: Session, assets: Assets):
        super().__init__(navigator, assets)
        self.session = session

        self.options: list[PauseOption] = list(PauseOption)

        self.set_screens()

    def input(self, key: int) -> None:
        match key:
            case keys.W | keys.UP:
                self.menu.move(1)
            case keys.S | keys.DOWN:
                self.menu.move(-1)
            case keys.ENTER:
                self._validate(self.menu.selected)
            case keys.ESCAPE:
                self._validate(1)

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

    def _validate(self, selected: int = 0) -> None:
        match self.options[selected]:
            case PauseOption.RESUME:
                self.session.game_state.switch_pause()
                self.navigator.pop()
            case PauseOption.MENU:
                self.session.new_game()
                self.navigator.back_to_menu()

    def draw_screen(self) -> None:
        self.title.draw()
        self.menu.draw()
