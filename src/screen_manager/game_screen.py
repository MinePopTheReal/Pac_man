from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.screen_manager.screen_manager import ScreenManager
from src.game_state.game_state import GameState, Direction, GameStatus
from src.rendering.hud_renderer import HudRenderer, MAX_SCORE_LENGHT
from src.rendering.entities_renderer import EntitiesRenderer
from src.utils.highscore_manager import HighscoreManager
from src.rendering.wall_renderer import WallRenderer
from src.utils.sprite_sheet_manager import Rotation
from src.rendering.assets import Assets, HUD_ZOOM, WALL_SIZE, ENTITIES_SIZE
from src.screen_manager.pause_screen import Pause
from src.screen_manager.end_game import EndGame
from src.screen_manager.screen import Screen
from src.parsing.models import GameConfig
from src.rendering.layer import Layer

from pyglet.window import key
from pyglet import clock, gl

class Play(Screen):
    def __init__(self, config: GameConfig, manager: ScreenManager, assets: Assets, highscores: HighscoreManager) -> None:
        super().__init__(manager, assets)
        self.config = config
        self.highscores = highscores
        self.game_state = GameState(config)

        self._current_level = -1

        self.maze_width = (
            self.config.width
            * WALL_SIZE
            * 3
        )        
        self.maze_height = (
            self.config.height
            * WALL_SIZE
            * 3
        )

        self.initial_hud_height = 2 * HUD_ZOOM + HUD_ZOOM

        # self.zoom = max(
        #     1,
        #     min(
        #         assets.screen_width // initial_maze_width,
        #         assets.screen_height // (initial_maze_height + self.initial_hud_height + 50),
        #     ),
        # )

        self.assets.wall_spritesheet.preloading_sprites(
            [Rotation.R0, Rotation.R90, Rotation.R180, Rotation.R270],
            WALL_SIZE,
        )
        self.assets.entities_spritesheet.preloading_sprites([Rotation.R0], ENTITIES_SIZE)
        self.assets.font_spritesheet.preloading_sprites([Rotation.R0], HUD_ZOOM)

        self.maze_pitch = (
            self.maze_width * assets.wall_spritesheet.bytes_number_per_pixel
        )
        self.entities_pitch = (
            self.maze_width * assets.entities_spritesheet.bytes_number_per_pixel
        )

        self.wall_layer = Layer(
            self.maze_width, self.maze_height, assets.wall_spritesheet.format
        )
        self.entities_layer = Layer(
            self.maze_width, self.maze_height, assets.entities_spritesheet.format
        )
        self.hud_height = self.initial_hud_height
        self.hud_layer = Layer(
            self.maze_width, self.hud_height, assets.font_spritesheet.format
        )

        self.hud_renderer = HudRenderer(self.game_state, assets.font_spritesheet, self.hud_layer, HUD_ZOOM)
        self.wall_renderer = WallRenderer(assets.wall_spritesheet)
        self.entities_renderer = EntitiesRenderer(
            self.game_state,
            self.entities_layer,
            assets.entities_spritesheet,
            assets.wall_spritesheet.bytes_number_per_pixel,
            ENTITIES_SIZE
        )

        total_height = self.maze_height + self.hud_height
        block_y = assets.window_height // 2 - total_height // 2

        self.maze_pos_x = assets.window_width // 2 - self.maze_width // 2
        self.maze_pos_y = block_y

        self.hud_pos_x = self.maze_pos_x
        self.hud_pos_y = self.maze_pos_y + self.maze_height

        clock.schedule_interval(self.entities_renderer.update_animation, 0.115)
        clock.schedule_interval(self.hud_renderer.update_hud, 0.2)

    def input(self, symbol: int) -> None:
        match symbol:
            case key.W | key.UP:
                self.game_state.select_direction(Direction.UP)
            case key.A | key.LEFT:
                self.game_state.select_direction(Direction.LEFT)
            case key.S | key.DOWN:
                self.game_state.select_direction(Direction.DOWN)
            case key.D | key.RIGHT:
                self.game_state.select_direction(Direction.RIGHT)
            case key.ESCAPE:
                self.game_state.switch_pause()
                self.manager.push(Pause(self.manager, self.game_state, self.assets))
            case key.T:
                self.game_state.switch_cheat_mode()
            case key.I:
                self.game_state.switch_invincible()
            case key.F:
                self.game_state.switch_ghosts_frozen()
            case key.N:
                self.game_state.skip_level()
            case key.L:
                self.game_state.add_extra_life()
            case key.V:
                self.game_state.switch_speed_pacman()
            case key.G:
                self.game_state.switch_slow_ghosts()

    def update_screen(self, dt: float) -> None:
        self.game_state.update(dt)

        status = self.game_state.status
        if status in [GameStatus.WON, GameStatus.LOST]:
            clock.unschedule(self.entities_renderer.update_animation)
            clock.unschedule(self.hud_renderer.update_hud)
            if status == GameStatus.WON:
                self.manager.pop()
                self.manager.push(EndGame(
                    self.manager,
                    True,
                    self.highscores,
                    self.game_state.score,
                    self.assets
                ))
            else:
                self.manager.pop()
                self.manager.push(EndGame(
                    self.manager, 
                    False, 
                    self.highscores,
                    self.game_state.score, 
                    self.assets
                ))

    def _build_maze(self) -> None:
        self.wall_renderer.create_maze_render(
            self.game_state.grid.cells, self.wall_layer.buffer_view, WALL_SIZE
        )
        self._current_level = self.game_state.level

    def draw_screen(self) -> None:
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        if self._current_level != self.game_state.level:
            self._build_maze()
        self.wall_layer.draw(self.maze_pos_x, self.maze_pos_y)
        self.entities_layer.draw(self.maze_pos_x, self.maze_pos_y)
        self.hud_layer.draw(self.hud_pos_x, self.hud_pos_y)

        self.entities_renderer.draw_entities()
