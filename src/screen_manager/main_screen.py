from src.screen_manager.screen import Screen, Navigator, ScreenName
from src.rendering.widget.label import Label
from src.rendering.widget.menu import Menu
from src.rendering.assets import (
    Assets,
    Layout,
    MAJOR_COLOR,
    MINOR_COLOR,
)


from pyglet.window import key as keys
from enum import Enum


class MainOptions(Enum):
    """Entries of the main menu.

    The value of each entry is the text shown in the menu. The order of
    the entries is the order of the menu, from top to bottom.
    """
    START = 'Start'
    HIGH_SCORES = 'Scores'
    INSTRUCTIONS = 'Rules'
    EXIT = 'Quit'


class MainScreen(Screen):
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
        assets: Assets,
        layout: Layout
    ) -> None:
        super().__init__(navigator, assets, layout)
        self.options: list[MainOptions] = list(MainOptions)

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

    def build_widget(self) -> None:
        """Build the title, the menu and the "press enter" text.

        Called when the screen is created and each time it is shown.
        The menu is made from the entries of Options.
        """
        self.title = Label(
            self.TITLE,
            self.layout.h1_px_size,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(self.assets.window_height - 200 * self.layout.scale_factor),
            anchor_x=0.5,
            anchor_y=1
        )

        title_bottom = self.title.y - self.title.height
        self.menu = Menu(
            [option.value for option in self.options],
            self.layout.h3_px_size,
            self.assets.font_spritesheet,
            MINOR_COLOR,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(title_bottom - 800 * self.layout.scale_factor),
            anchor_x=0.5,
            anchor_y=0
        )

        menu_bottom = self.menu.y - self.menu.height
        self.helper_text = Label(
            "press enter",
            self.layout.h3_px_size,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(menu_bottom + 200 * self.layout.scale_factor),
            anchor_x=0.5,
            anchor_y=1,
            blink_period=0.4
        )

    def _validate(self, selected: int) -> None:
        """Run the action of a menu entry.

        Start, Scores and Rules open the matching screen on top of this
        one, and Quit closes the game.

        Args:
            selected (int): The position of the chosen entry in the menu.
        """
        match self.options[selected]:
            case MainOptions.START:
                self.navigator.push(ScreenName.GAME_SCREEN)
            case MainOptions.HIGH_SCORES:
                self.navigator.push(ScreenName.HIGH_SCORE)
            case MainOptions.INSTRUCTIONS:
                self.navigator.push(ScreenName.INSTRUCTIONS)
            case MainOptions.EXIT:
                self.navigator.quit()

    def draw_screen(self) -> None:
        """Draw the menu, the title and the "press enter" text."""
        self.menu.draw()
        self.title.draw()
        self.helper_text.draw()
