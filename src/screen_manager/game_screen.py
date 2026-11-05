from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager

from src.game_state.game_state import GameState, Direction, GameStatus
from src.utils.highscore_manager import HighscoreManager
from src.screen_manager.pause_screen import Pause
from src.screen_manager.end_game import EndGame
from src.screen_manager.screen import Screen
from src.utils.widget.maze_view import MazeView
from src.utils.widget.hud import Hud
from src.parsing.models import GameConfig
from src.rendering.assets import Assets, H4_PX_SIZE, MAJOR_COLOR, SCALE_FACTOR, H5_PX_SIZE

from pyglet.window import key

HUD_MARGIN_PX = 10

DIRECTION_KEYS = {
    key.W: Direction.UP, key.UP: Direction.UP,
    key.A: Direction.LEFT, key.LEFT: Direction.LEFT,
    key.S: Direction.DOWN, key.DOWN: Direction.DOWN,
    key.D: Direction.RIGHT, key.RIGHT: Direction.RIGHT,
}

class Play(Screen):
    def __init__(
        self,
        config: GameConfig,
        manager: ScreenManager,
        assets: Assets,
        highscores: HighscoreManager,
    ) -> None:
        super().__init__(manager, assets)
        self.highscores = highscores
        self.game_state = GameState(config)

        center_x = assets.window_width // 2
        center_y = assets.window_height // 2

        self.maze_view = MazeView(
            self.game_state,
            assets,
            config,
            x=center_x,
            y=center_y
        )

        maze_view_top = self.maze_view.bottom + self.maze_view.height
        self.hud = Hud(
            H4_PX_SIZE,
            assets.font_spritesheet,
            MAJOR_COLOR,
            x=center_x,
            y=maze_view_top + HUD_MARGIN_PX * SCALE_FACTOR,
            anchor_x=0.5,
            anchor_y=0,
        )

        self._cheat_actions = {
            key.C: self.game_state.switch_cheat_mode,
            key._1: self.game_state.switch_invincible,
            key._2: self.game_state.switch_ghosts_frozen,
            key._3: self.game_state.skip_level,
            key._4: self.game_state.add_extra_life,
            key._5: self.game_state.switch_speed_pacman,
            key._6: self.game_state.switch_slow_ghosts,
        }

        self.maze_view.start_animation()

    def input(self, symbol: int) -> None:
        if symbol in DIRECTION_KEYS:
            self.game_state.select_direction(DIRECTION_KEYS[symbol])
        elif symbol == key.ESCAPE:
            self.game_state.switch_pause()
            self.manager.push(Pause(self.manager, self.game_state, self.assets))
        elif symbol in self._cheat_actions:
            self._cheat_actions[symbol]()

    def update_screen(self, dt: float) -> None:
        self.game_state.update(dt)

        status = self.game_state.status
        if status not in (GameStatus.WON, GameStatus.LOST):
            return

        self.maze_view.stop_animation()
        self.manager.pop()
        self.manager.push(EndGame(
            self.manager,
            status == GameStatus.WON,
            self.highscores,
            self.game_state.score,
            self.assets,
        ))

    def draw_screen(self) -> None:
        self.maze_view.draw()
        self.hud.set_state(self.game_state)
        self.hud.draw()