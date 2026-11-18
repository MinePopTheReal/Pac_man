from src.screen_manager.screen import Screen, Navigator, ScreenName
from src.rendering.widget.maze_view import MazeView, TILES_PER_CELL
from src.rendering.assets import Assets, H4_PX_SIZE, MAJOR_COLOR
from src.utils.high_score_manager import HighScoreManager
from src.game.game_state import GameStatus
from src.entity.direction import Direction
from src.message.errors import RenderError
from src.rendering.widget.hud import Hud
from src.game.session import Session


from pyglet.window import key


HUD_MARGIN_PX = 10
TOP_AND_BOTTOM_MARGIN = 75

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


class GameScreen(Screen):
    """Screen where the game is played.

    It shows the maze and the HUD, sends the keys pressed to the game,
    makes the game move forward each frame, and goes to the end screen
    when the game is won or lost.
    """
    def __init__(
        self,
        navigator: Navigator,
        high_score: HighScoreManager,
        session: Session,
        assets: Assets,
    ) -> None:
        super().__init__(navigator, assets)
        self.high_score = high_score
        self.session = session

    def build_widget(self) -> None:
        """Build the maze view and the HUD for the current game.

        Called each time the screen is shown, so the widgets always match
        the game of the session. The maze is centered in the window and
        the HUD is placed just above it.
        """
        win_w = self.assets.window_width
        win_h = self.assets.window_height
        config = self.session.config

        self.hud = Hud(
            H4_PX_SIZE,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=0,
            y=0,
            anchor_x=0.5,
            anchor_y=0,
        )
        margin = self.hud.zoom // 2

        tiles_w = config.width * TILES_PER_CELL
        tiles_h = config.height * TILES_PER_CELL
        free_h = win_h - self.hud.height - margin - TOP_AND_BOTTOM_MARGIN * 2

        wall_size = min(win_w // tiles_w, free_h // tiles_h)
        min_wall_size = \
            self.assets.wall_spritesheet.spritesheet_config.tile_size

        if (wall_size < min_wall_size or self.hud.width > win_w):
            raise RenderError(
                f"Maze {config.width}x{config.height} too large for a "
                f"{win_w}x{win_h} window"
            )
        entity_size = wall_size * 2

        self.maze_view = MazeView(
            self.session.game_state,
            self.assets,
            config,
            wall_size,
            entity_size,
            x=0, y=0,
        )

        block_h = self.maze_view.height + margin + self.hud.height
        block_bottom = (win_h - block_h) // 2

        self.maze_view.x = win_w // 2
        self.maze_view.y = block_bottom + int(
            self.maze_view.anchor_y * self.maze_view.height
        )

        self.hud.x = win_w // 2
        self.hud.y = block_bottom + self.maze_view.height + margin

    def _cheat_action(self, symbol: int) -> None:
        """Run the cheat linked to a key, if there is one.

        C turns the cheat mode on or off, and 1 to 6 switch the other
        cheats (they do nothing while the cheat mode is off). The game
        is read again at each key press, so the cheats also work after
        a new game was started. Other keys are ignored.

        Args:
            symbol (int): The code of the key (see pyglet.window.key).
        """
        gs = self.session.game_state
        actions = {
            key.C: gs.switch_cheat_mode,
            key._1: gs.switch_invincible,
            key._2: gs.switch_ghosts_frozen,
            key._3: gs.skip_level,
            key._4: gs.add_extra_life,
            key._5: gs.switch_speed_pacman,
            key._6: gs.switch_slow_ghosts
        }

        if symbol in actions:
            actions[symbol]()

    def input(self, symbol: int) -> None:
        """Handle a key pressed during the game.

        WASD and the arrow keys choose the direction of Pac-Man, Escape
        pauses the game and opens the pause screen, and any other key is
        tried as a cheat key.

        Args:
            symbol (int): The code of the key (see pyglet.window.key).
        """
        if symbol in DIRECTION_KEYS:
            self.session.game_state.select_direction(DIRECTION_KEYS[symbol])
        elif symbol == key.ESCAPE:
            self.session.game_state.switch_pause()
            self.navigator.push(ScreenName.PAUSE)
        else:
            self._cheat_action(symbol)

    def update_screen(self, dt: float) -> None:
        """Move the maze animation and the game forward by one frame.

        When the game is won or lost, this screen is replaced by the end
        screen.

        Args:
            dt (float): Seconds since the last frame.
        """
        self.maze_view.update(dt)
        self.session.game_state.update(dt)

        status = self.session.game_state.status
        if status not in (GameStatus.WON, GameStatus.LOST):
            return

        self.navigator.pop()
        self.navigator.push(ScreenName.ENDGAME)

    def draw_screen(self) -> None:
        """Draw the maze, then the HUD with the current state of the game."""
        self.maze_view.draw()
        self.hud.set_state(self.session.game_state)
        self.hud.draw()
