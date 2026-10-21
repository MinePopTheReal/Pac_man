from src.screen_manager.screen import Screen
# from collections import deque


class ScreenManager:
    def __init__(self, main_screen: Screen) -> None:
        self.main_screen = main_screen
        self.screens: list[Screen] = [self.main_screen]
        self.should_exit: bool = False

    def current_screen(self, main_screen: Screen) -> Screen:
        return self.screens[-1]

    def push(self, screen: Screen) -> None:
        self.screens.append(screen)

    def pop(self) -> None:
        if len(self.screens) > 1:
            self.screens.pop()

    def back_to_menu(self,  main_screen: Screen) -> None:
        for i in range(len(self.screens) - 1, -1, -1):
            if self.screens[i] != main_screen:
                self.screens.pop()

    def quit(self) -> None:
        self.should_exit = True

    def input_key(self, key) -> None:
        ...

    def update(self, dt: float) -> None:
        ...

    def draw(self) -> None:
        ...
