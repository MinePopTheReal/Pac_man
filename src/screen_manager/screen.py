from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
    from src.rendering.assets import Assets



class Screen(ABC):

    def __init__(self, manager: ScreenManager, assets: Assets) -> None:
        self.manager = manager
        self.assets = assets

    @abstractmethod
    def input(self, key: int) -> None:
        ...

    def update_screen(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw_screen(self) -> None:
        ...
