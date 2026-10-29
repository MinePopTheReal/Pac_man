# TEMPORARY: This file is intended solely for testing the graphics rendering
# (sprite sheets, layers, HUD). The input loop and the drawing loop are
# placeholder code; we need to wait for the screen manager and the screens to
# finalize the display and implement this section of code properly.
from __future__ import annotations

from src.screen_manager.screen_manager import ScreenManager


from pyglet import window, display, clock

# HUD_ZOOM_FACTOR = 2
SCREEN_MARGIN = 0.95

class Display(window.Window):
    def __init__(self, screen_manager: ScreenManager):

        display_data = display.get_display()
        screen = display_data.get_default_screen()
        clock.schedule_interval(self.update, 1 / 60)

        super().__init__(
            width=round(screen.width * SCREEN_MARGIN),
            height=round(screen.height * SCREEN_MARGIN),
            caption="Pac-Man",
        )

        self.screen_manager = screen_manager

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.screen_manager.current_screen.input(symbol)

    def on_draw(self) -> None:
        self.clear()
        self.screen_manager.current_screen.draw_screen()

    def update(self, dt: float) -> None:
        self.screen_manager.update(dt)
