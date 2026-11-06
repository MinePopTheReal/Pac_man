from src.screen_manager.screen import Screen, ScreenName
from src.message.errors import ScreenError


from pyglet import app


class ScreenManager:
    def __init__(self) -> None:
        self.main_screen_name: ScreenName | None = None
        self.screens_stack: list[Screen] = []
        self.screens: dict[ScreenName, Screen] = {}

    def first_screen(self, screen_name: ScreenName) -> None:
        self.push(screen_name)
        self.main_screen_name = screen_name

    def register_screens(self, name: ScreenName, screen: Screen) -> None:
        self.screens[name] = screen

    @property
    def current_screen(self) -> Screen:
        if not self.screens_stack:
            raise ScreenError("first_screen() must be called first")
        return self.screens_stack[-1]

    def push(self, screen_name: ScreenName) -> None:
        screen = self.screens.get(screen_name)
        if not screen:
            raise ScreenError(
                "The screenshot you want to push isn't registered."
            )
        screen.set_screens()
        self.screens_stack.append(screen)

    def pop(self) -> None:
        if len(self.screens_stack) > 1:
            self.screens_stack.pop()

    def back_to_menu(self) -> None:
        if self.main_screen_name is None:
            raise ScreenError(
                "first_screen() must be called " "before back_to_menu()"
            )
        self.screens_stack.clear()
        self.push(self.main_screen_name)

    def quit(self) -> None:
        app.exit()

    def update(self, dt: float) -> None:
        self.current_screen.update_screen(dt)
