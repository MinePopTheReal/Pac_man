from src.rendering.assets import Assets


from abc import ABC, abstractmethod
from typing import Protocol
from enum import StrEnum


class ScreenName(StrEnum):
    """Names of the screens of the game.

    They are used to register a screen in the screen manager and to ask
    it to show a screen.
    """
    MAIN = "main"
    PLAY = "play"
    INSTRUCTION = "instruction"
    HIGH_SCORE = "high_score"
    PAUSE = "pause"
    ENDGAME = "endgame"


class Navigator(Protocol):
    """What a screen needs to be able to change screen.

    A screen only knows this interface, not the real screen manager,
    so it does not depend on how the screens are stored.
    """
    def push(self, screen_name: ScreenName) -> None:
        """Show a screen on top of the current one.

        Args:
            screen_name (ScreenName): The name of the screen to show.
        """
        ...

    def pop(self) -> None:
        """Remove the current screen and show the one below it."""
        ...

    def quit(self) -> None:
        """End the game."""
        ...

    def back_to_menu(self) -> None:
        """Remove all the screens and show the first screen again."""
        ...


class Screen(ABC):
    """Base class of all the screens of the game.

    A screen builds its widgets, reacts to the keys pressed, can be
    updated each frame and draws itself. The screen manager calls these
    methods on the screen at the top of its stack.
    """
    def __init__(self, navigator: Navigator, assets: Assets) -> None:
        self.navigator = navigator
        self.assets = assets

    @abstractmethod
    def set_screens(self) -> None:
        """Build the widgets of the screen.

        Called by the screen manager each time the screen is shown, so
        the widgets are always up to date.
        """
        ...

    @abstractmethod
    def input(self, key: int) -> None:
        """Handle a key pressed while the screen is shown.

        Args:
            key (int): The code of the key (see pyglet.window.key).
        """
        ...

    def update_screen(self, dt: float) -> None:
        """Make the screen move forward by one frame.

        Does nothing by default. A screen that has something to update
        (a blinking text, the game) overrides it.

        Args:
            dt (float): Seconds since the last frame.
        """
        pass

    @abstractmethod
    def draw_screen(self) -> None:
        """Draw the screen in the window."""
        ...
