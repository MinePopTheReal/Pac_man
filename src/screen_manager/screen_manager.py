from src.screen_manager.screen import Screen, ScreenName
from src.message.errors import ScreenError


from pyglet import app


class ScreenManager:
    """Keeps the screens of the game and knows which one is shown.

    The shown screens are kept in a stack: the screen at the top is the
    current one and receives the input, the updates and the drawing.
    Pushing a screen puts it on top of the others (for example the pause
    on top of the game), and popping it shows the one below again.
    """
    def __init__(self) -> None:
        self.main_screen_name: ScreenName | None = None
        self.screens_stack: list[Screen] = []
        self.screens: dict[ScreenName, Screen] = {}

    def first_screen(self, screen_name: ScreenName) -> None:
        """Show the first screen of the game and remember it as the menu.

        Args:
            screen_name (ScreenName): The name of a registered screen.

        Raises:
            ScreenError: If the screen was not registered.
        """
        self.push(screen_name)
        self.main_screen_name = screen_name

    def register_screens(self, name: ScreenName, screen: Screen) -> None:
        """Register a screen so it can be shown later by its name.

        Args:
            name (ScreenName): The name used to push the screen.
            screen (Screen): The screen to register.
        """
        self.screens[name] = screen

    @property
    def current_screen(self) -> Screen:
        """Screen at the top of the stack, the one currently shown.

        Raises:
            ScreenError: If no screen was shown yet (first_screen() was
                not called).
        """
        if not self.screens_stack:
            raise ScreenError("first_screen() must be called first")
        return self.screens_stack[-1]

    def push(self, screen_name: ScreenName) -> None:
        """Show a screen on top of the current one.

        The screen builds its widgets (set_screens) just before being
        shown. The current screen stays in the stack, so pop() can show
        it again.

        Args:
            screen_name (ScreenName): The name of a registered screen.

        Raises:
            ScreenError: If the screen was not registered.
        """
        screen = self.screens.get(screen_name)
        if not screen:
            raise ScreenError(
                "The screen you want to push isn't registered."
            )
        screen.set_screens()
        self.screens_stack.append(screen)

    def pop(self) -> None:
        """Remove the current screen and show the one below it.

        Does nothing when only one screen is left, so the stack never
        becomes empty.
        """
        if len(self.screens_stack) > 1:
            self.screens_stack.pop()

    def back_to_menu(self) -> None:
        """Remove all the screens and show the first screen again.

        Raises:
            ScreenError: If first_screen() was not called before.
        """
        if self.main_screen_name is None:
            raise ScreenError(
                "first_screen() must be called " "before back_to_menu()"
            )
        self.screens_stack.clear()
        self.push(self.main_screen_name)

    def quit(self) -> None:
        """Stop the pyglet event loop, which ends the game."""
        app.exit()

    def update(self, dt: float) -> None:
        """Update the current screen.

        Only the screen at the top of the stack is updated: the screens
        below it are paused.

        Args:
            dt (float): Seconds since the last update.
        """
        self.current_screen.update_screen(dt)
