from src.rendering.assets import MINIMAL_RESOLUTION
from src.screen_manager.screen_manager import ScreenManager
from src.message.warning_message import WarningMessage
from src.message.errors import RenderError


from pyglet.window import Window
from pyglet import clock


class Display(Window):
    """
    Main class for managing the display; it centralizes input,
    determines what to display, and updates the screens
    """
    def __init__(self, screen_manager: ScreenManager, width: int, height: int):
        """
        Runs the screen update and returns errors and warnings based on
        the resolution to alert the user to a potential display issue
        """
        clock.schedule_interval(self.update, 1 / 60)
        if (
            width < MINIMAL_RESOLUTION[0]
            or height < MINIMAL_RESOLUTION[1]
        ):
            raise RenderError(
                "Your resolution is too low. " "The game is unplayable"
            )
        if (width / 16) * 9 != height:
            print(
                WarningMessage(
                    "Your resolution is not 16:9. "
                    "Display distortion may occur."
                )
            )

        super().__init__(
            width=round(width),
            height=round(height),
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
