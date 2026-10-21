from src.screen_manager.screen import Screen


class ScreenManager:
    def __init__(self, screens: list[Screen]) -> None:
        self.screens = screens
        self.should_exit: bool = False

    def current_screen(self, screen: Screen) -> Screen:
        if not self.screens:
            self.screens.append(screen)
        return self.screens[-1]

    def push(self) -> None:
        ...

    def pop(self) -> None:
        ...

    def back_to_menu(self,  screen: Screen) -> None:
        ...

    def quit(self) -> None:
        self.should_exit = True

    def input_key(self, key) -> None:
        ...

    def update(self, dt: float) -> None:
        ...

    def draw(self) -> None:
        ...
