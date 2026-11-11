from src.screen_manager.screen import Screen, Navigator
from src.rendering.widget.label import Label
from src.rendering.widget.menu import Menu
from src.game.session import Session
from src.rendering.assets import (
    Assets,
    H1_PX_SIZE,
    H3_PX_SIZE,
    MAJOR_COLOR,
    MINOR_COLOR,
    SCALE_FACTOR
)


from pyglet.window import key as keys
from enum import Enum


class PauseOption(Enum):
    """Entries of the pause menu.

    The value of each entry is the text shown in the menu. The order of
    the entries is the order of the menu, from top to bottom.
    """
    RESUME = 'Resume'
    MENU = 'Back to menu'


class PauseScreen(Screen):
    """Screen shown on top of the game when the player pauses it.

    It shows a menu to resume the game or to give it up and go back to
    the main menu.

    Attributes:
        TITLE (str): The title displayed at the top of the screen.
        options (list[PauseOption]): The entries of the menu, in order.
    """
    TITLE = "pause"

    def __init__(self, navigator: Navigator, session: Session, assets: Assets):
        super().__init__(navigator, assets)
        self.session = session

        self.options: list[PauseOption] = list(PauseOption)

    def input(self, key: int) -> None:
        """Handle a key pressed in the pause menu.

        W or Up selects the previous entry, S or Down selects the next
        one, Enter runs the selected entry, and Escape resumes the game.
        Other keys are ignored.

        Args:
            key (int): The code of the key (see pyglet.window.key).
        """
        match key:
            case keys.W | keys.UP:
                self.menu.move(-1)
            case keys.S | keys.DOWN:
                self.menu.move(1)
            case keys.ENTER:
                self._validate(self.menu.selected)
            case keys.ESCAPE:
                self._validate(0)

    def build_widget(self) -> None:
        """Build the title and the menu.

        Called when the screen is created and each time it is shown.
        The menu is made from the entries of PauseOption.
        """
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
        """Run the action of a menu entry.

        Resume unpauses the game and closes this screen. Back to menu
        gives up the current game, prepares a new one, and goes back to
        the main menu.

        Args:
            selected (int): The position of the chosen entry in the menu.
                The default is the first entry (Resume).
        """
        match self.options[selected]:
            case PauseOption.RESUME:
                self.session.game_state.switch_pause()
                self.navigator.pop()
            case PauseOption.MENU:
                self.session.new_game()
                self.navigator.back_to_menu()

    def draw_screen(self) -> None:
        """Draw the title and the menu."""
        self.title.draw()
        self.menu.draw()
