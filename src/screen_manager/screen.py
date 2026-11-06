from src.rendering.assets import Assets


from abc import ABC, abstractmethod
from typing import Protocol
from enum import StrEnum


class ScreenName(StrEnum):
    MAIN = "main"
    PLAY = "play"
    INSTRUCTION = "instruction"
    HIGHSCORE = "high_score"
    PAUSE = "pause"
    ENDGAME = "endgame"


class Navigator(Protocol):
    def push(self, screen_name: ScreenName) -> None:
        ...

    def pop(self) -> None:
        ...

    def quit(self) -> None:
        ...

    def back_to_menu(self) -> None:
        ...


class Screen(ABC):
    def __init__(self, navigator: Navigator, assets: Assets) -> None:
        self.navigator = navigator
        self.assets = assets

    @abstractmethod
    def set_screens(self) -> None:
        ...

    @abstractmethod
    def input(self, key: int) -> None:
        ...

    def update_screen(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw_screen(self) -> None:
        ...
