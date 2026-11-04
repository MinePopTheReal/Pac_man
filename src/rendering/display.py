from __future__ import annotations

from src.screen_manager.screen_manager import ScreenManager
from src.message.warning import WarningMessage
from src.message.errors import RenderError

from pyglet import window, display, clock

SCREEN_MARGIN = 0.95

REFERENCE_RESOLUTION = (3840 * SCREEN_MARGIN, 2160 * SCREEN_MARGIN)
SCREEN = display.get_display().get_default_screen()
# ACTUAL_RESOLUTION = (240 * SCREEN_MARGIN, 320 * SCREEN_MARGIN)
ACTUAL_RESOLUTION = (SCREEN.width * SCREEN_MARGIN, SCREEN.height * SCREEN_MARGIN)

SCALE_FACTOR = max(0.1, min(ACTUAL_RESOLUTION[0] / REFERENCE_RESOLUTION[0], ACTUAL_RESOLUTION[1] / REFERENCE_RESOLUTION[1]))

MINIMAL_RESOLUTION = (854 * SCREEN_MARGIN, 480 * SCREEN_MARGIN)


class Display(window.Window):
    def __init__(self, screen_manager: ScreenManager):

        clock.schedule_interval(self.update, 1 / 60)
        if ACTUAL_RESOLUTION[0] < MINIMAL_RESOLUTION[0] or ACTUAL_RESOLUTION[1] < MINIMAL_RESOLUTION[1]:
            raise RenderError(
                "Your resolution is too low. "
                "The game may not be playable."
            )
        if (ACTUAL_RESOLUTION[0] / 16) * 9 != ACTUAL_RESOLUTION[1]:
            print(WarningMessage(
                "Your resolution is not 16:9. "
                "Display distortion may occur."
            ))

        super().__init__(
            width=round(ACTUAL_RESOLUTION[0]),
            height=round(ACTUAL_RESOLUTION[1]),
            caption="Pac-Man"
        )

        self.screen_manager = screen_manager

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.screen_manager.current_screen.input(symbol)

    def on_draw(self) -> None:
        self.clear()
        self.screen_manager.current_screen.draw_screen()

    def update(self, dt: float) -> None:
        self.screen_manager.update(dt)
