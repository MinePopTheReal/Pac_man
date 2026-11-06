from src.rendering.assets import Assets, H4_PX_SIZE, MAJOR_COLOR, SCALE_FACTOR
from src.game_state.game_state import Direction, GameStatus
from src.screen_manager.screen_manager import ScreenName
from src.utils.high_score_manager import HighScoreManager
from src.screen_manager.screen import Screen, Navigator
from src.utils.widget.maze_view import MazeView
from src.game_state.session import Session
from src.utils.widget.hud import Hud


from pyglet.window import key


HUD_MARGIN_PX = 10

DIRECTION_KEYS = {
    key.W: Direction.UP,
    key.UP: Direction.UP,
    key.A: Direction.LEFT,
    key.LEFT: Direction.LEFT,
    key.S: Direction.DOWN,
    key.DOWN: Direction.DOWN,
    key.D: Direction.RIGHT,
    key.RIGHT: Direction.RIGHT,
}


class Play(Screen):
    def __init__(
        self,
        session: Session,
        navigator: Navigator,
        assets: Assets,
        high_score: HighScoreManager,
    ) -> None:
        super().__init__(navigator, assets)
        self.high_score = high_score
        self.session = session

        self._cheat_actions = {
            key.C: self.session.game_state.switch_cheat_mode,
            key._1: self.session.game_state.switch_invincible,
            key._2: self.session.game_state.switch_ghosts_frozen,
            key._3: self.session.game_state.skip_level,
            key._4: self.session.game_state.add_extra_life,
            key._5: self.session.game_state.switch_speed_pacman,
            key._6: self.session.game_state.switch_slow_ghosts,
        }

        self.set_screens()

    def set_screens(self) -> None:
        center_x = self.assets.window_width // 2
        center_y = self.assets.window_height // 2

        self.maze_view = MazeView(
            self.session.game_state,
            self.assets,
            self.session.config,
            x=center_x,
            y=center_y,
        )

        maze_view_top = self.maze_view.bottom + self.maze_view.height
        self.hud = Hud(
            H4_PX_SIZE,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=center_x,
            y=int(maze_view_top + HUD_MARGIN_PX * SCALE_FACTOR),
            anchor_x=0.5,
            anchor_y=0,
        )

        self.maze_view.start_animation()

    def input(self, symbol: int) -> None:
        if symbol in DIRECTION_KEYS:
            self.session.game_state.select_direction(DIRECTION_KEYS[symbol])
        elif symbol == key.ESCAPE:
            self.session.game_state.switch_pause()
            self.navigator.push(ScreenName.PAUSE)
        elif symbol in self._cheat_actions:
            self._cheat_actions[symbol]()

    def update_screen(self, dt: float) -> None:
        self.session.game_state.update(dt)

        status = self.session.game_state.status
        if status not in (GameStatus.WON, GameStatus.LOST):
            return

        self.maze_view.stop_animation()
        self.navigator.pop()
        self.navigator.push(ScreenName.ENDGAME)

    def draw_screen(self) -> None:
        self.maze_view.draw()
        self.hud.set_state(self.session.game_state)
        self.hud.draw()
