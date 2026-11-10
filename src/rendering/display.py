from src.rendering.assets import ACTUAL_RESOLUTION, MINIMAL_RESOLUTION
from src.screen_manager.screen_manager import ScreenManager
from src.message.warning_message import WarningMessage
from src.message.errors import RenderError


from pyglet import window, clock


class Display(window.Window):
    """
    Main class for managing the display; it centralizes input,
    determines what to display, and updates the screens
    """
    def __init__(self, screen_manager: ScreenManager):
        """
        Runs the screen update and returns errors and warnings based on
        the resolution to alert the user to a potential display issue
        """
        clock.schedule_interval(self.update, 1 / 60)
        if (
            ACTUAL_RESOLUTION[0] < MINIMAL_RESOLUTION[0]
            or ACTUAL_RESOLUTION[1] < MINIMAL_RESOLUTION[1]
        ):
            raise RenderError(
                "Your resolution is too low. " "The game is unplayable"
            )
        if (ACTUAL_RESOLUTION[0] / 16) * 9 != ACTUAL_RESOLUTION[1]:
            print(
                WarningMessage(
                    "Your resolution is not 16:9. "
                    "Display distortion may occur."
                )
            )

        super().__init__(
            width=round(ACTUAL_RESOLUTION[0]),
            height=round(ACTUAL_RESOLUTION[1]),
            caption="Pac-Man",
        )

        self.screen_manager = screen_manager

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Send a key press to the current screen.

        Args:
            symbol (int): The key code (see pyglet.window.key).
            modifiers (int): The modifier keys held down (Shift, Ctrl...).
                Not used by the game.
        """
        self.screen_manager.current_screen.input(symbol)

    def on_draw(self) -> None:
        """
        Clear the window and draw the current screen.
        """
        self.clear()
        self.screen_manager.current_screen.draw_screen()

    def update(self, dt: float) -> None:
        """Update the current screen.

        Args:
            dt (float): Seconds since the last update.
        """
        self.screen_manager.update(dt)
