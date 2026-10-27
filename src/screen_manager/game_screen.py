from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.screen import Screen
from src.game_state.game_state import GameState, Direction, GameStatus
from src.parsing.models import GameConfig
from pyglet.window import key as keys
from src.screen_manager.pause_screen import Pause
from src.screen_manager.end_game import EndGame
from src.utils.highscore_manager import HighscoreManager


class Play(Screen):
    def __init__(self, config: GameConfig, manager: ScreenManager,
                 highscores: HighscoreManager):
        super().__init__(manager)
        self.config = config
        self.game = GameState(self.config)
        self.highscores = highscores

    def input(self, key: int) -> None:
        match key:
            case keys.W | keys.UP:
                self.game.select_direction(Direction.UP)
            case keys.A | keys.LEFT:
                self.game.select_direction(Direction.LEFT)
            case keys.S | keys.DOWN:
                self.game.select_direction(Direction.DOWN)
            case keys.D | keys.RIGHT:
                self.game.select_direction(Direction.RIGHT)
            case keys.ESCAPE:
                self.game.switch_pause()
                self.manager.push(Pause(self.manager, self.game))
            case keys.T:
                self.game.switch_cheat_mode()
            case keys.I:
                self.game.switch_invincible()
            case keys.F:
                self.game.switch_ghosts_frozen()
            case keys.N:
                self.game.skip_level()
            case keys.L:
                self.game.add_extra_life()
            case keys.V:
                self.game.switch_speed_pacman()
            case keys.G:
                self.game.switch_slow_ghosts()

    def update_screen(self, dt: float) -> None:
        self.game.update(dt)

        status = self.game.status
        if status == GameStatus.WON:
            self.manager.pop()
            self.manager.push(EndGame(self.manager, True, self.highscores,
                                      self.game.score))

        elif status == GameStatus.LOST:
            self.manager.pop()
            self.manager.push(EndGame(self.manager, False, self.highscores,
                                      self.game.score))

    def draw_screen(self) -> None:
        ...
