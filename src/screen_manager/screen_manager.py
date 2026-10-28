from __future__ import annotations
from src.screen_manager.screen import Screen
from src.message.errors import ScreenError


class ScreenManager:
    def __init__(self) -> None:
        self.main_screen: Screen | None = None
        self.screens: list[Screen] = []
        self.should_exit: bool = False

    def first_screen(self, menu: Screen) -> None:
        self.screens.append(menu)
        self.main_screen = menu

    @property
    def current_screen(self) -> Screen:
        if not self.screens:
            raise ScreenError("first_screen() must be called first")
        return self.screens[-1]

    def push(self, screen: Screen) -> None:
        screen.reset()
        self.screens.append(screen)

    def pop(self) -> None:
        if len(self.screens) > 1:
            self.screens.pop()

    def back_to_menu(self) -> None:
        if self.main_screen is None:
            raise ScreenError("first_screen() must be called "
                              "before back_to_menu()")
        self.screens.clear()
        self.push(self.main_screen)

    def quit(self) -> None:
        self.should_exit = True

    def input_key(self, key: int) -> None:
        self.current_screen.input(key)

    def update(self, dt: float) -> None:
        self.current_screen.update_screen(dt)

    def draw(self) -> None:
        ...
