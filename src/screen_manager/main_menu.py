from src.screen_manager.screen_manager import ScreenName
from src.screen_manager.screen import Screen, Navigator
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
    """Entries of the main menu.

    The value of each entry is the text shown in the menu. The order of
    the entries is the order of the menu, from top to bottom.
    """
    START = 'Start'
    HIGH_SCORES = 'Scores'
    INSTRUCTIONS = 'Rules'
    EXIT = 'Quit'


class MainMenu(Screen):
    """First screen of the game, where the player chooses what to do.

    It shows the title and a menu to start a game, see the high scores,
    read the instructions or quit. A "press enter" text blinks under
    the menu.

    Attributes:
        TITLE (str): The title displayed at the top of the screen.
        options (list[Options]): The entries of the menu, in order.
    """
    TITLE = "PAC-MAN"

    def __init__(
        self,
        navigator: Navigator,
        assets: Assets
    ) -> None:
        super().__init__(navigator, assets)
        self.options: list[Options] = list(Options)

        self.set_screens()

    def update_screen(self, dt: float) -> None:
        """Make the "press enter" text blink.

        Args:
            dt (float): Seconds since the last frame.
        """
        self.helper_text.update(dt)

    def input(self, key: int) -> None:
        """Handle a key pressed in the menu.

        W or Up selects the previous entry, S or Down selects the next
        one, Enter opens the selected entry, and Escape quits the game.
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
                self.navigator.quit()

    def set_screens(self) -> None:
        """Build the title, the menu and the "press enter" text.

        Called when the screen is created and each time it is shown.
        The menu is made from the entries of Options.
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
        """Run the action of a menu entry.

        Start, Scores and Rules open the matching screen on top of this
        one, and Quit closes the game.

        Args:
            selected (int): The position of the chosen entry in the menu.
        """
        match self.options[selected]:
            case Options.START:
                self.navigator.push(ScreenName.PLAY)
            case Options.HIGH_SCORES:
                self.navigator.push(ScreenName.HIGH_SCORE)
            case Options.INSTRUCTIONS:
                self.navigator.push(ScreenName.INSTRUCTION)
            case Options.EXIT:
                self.navigator.quit()

    def draw_screen(self) -> None:
        """Draw the menu, the title and the "press enter" text."""
        self.menu.draw()
        self.title.draw()
        self.helper_text.draw()
