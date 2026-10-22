from src.screen_manager.screen import Screen


class ScreenManager:
    def __init__(self, main_screen: Screen) -> None:
        self.main_screen = main_screen
        self.screens: list[Screen] = [self.main_screen]
        self.should_exit: bool = False

    @property
    def current_screen(self) -> Screen:
        return self.screens[-1]

    def push(self, screen: Screen) -> None:
        self.screens.append(screen)

    def pop(self) -> None:
        if len(self.screens) > 1:
            self.screens.pop()

    def back_to_menu(self) -> None:
        self.screens.clear()
        self.screens.append(self.main_screen)

    def quit(self) -> None:
        self.should_exit = True

    def input_key(self, key: int) -> None:
        self.current_screen.input(key)

    def update(self, dt: float) -> None:
        self.current_screen.update_screen(dt)

    def draw(self) -> None:
        ...


# if __name__ == "__main__":
#     from src.screen_manager.screen import Screen

#     class Test(Screen):
#         def __init__(self, name):
#             self.name = name

#         def input(self, key):
#             print(self.name, 'reçoit la touche', key)

#         def update_screen(self, dt):
#             print(self.name, 'reçoit dt =', dt)

#         def draw_screen(self):
#             pass

#     t = Test('menu')
#     m = ScreenManager(t)
#     m.input_key(5)
#     m.update(0.1)
#     m.push(Test('jeu'))
#     m.input_key(7)
#     m.update(0.2)
