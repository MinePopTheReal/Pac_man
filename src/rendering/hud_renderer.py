from src.rendering.layer import Layer
from src.utils.sprite_sheet_manager import SpriteSheetManager, Rotation
from src.game_state.game_state import GameState

from typing import Any


class HudRenderer:
    def __init__(self, game_state: GameState, spritesheet: SpriteSheetManager, layer: Layer, zoom: int):
        self.game_state: GameState = game_state
        self.spritesheet: SpriteSheetManager = spritesheet
        self.layer: Layer = layer
        self.zoom = zoom

        self.game_values = {
            "time": (lambda: self.game_state.level_time_left, 0, 0),
            "lives": (lambda: self.game_state.lives, 0, 1),
            "level": (lambda: self.game_state.level, 0, 2),
            "score": (lambda: self.game_state.score, 0, 3)
        }


        self.last_hud_info: dict[str, Any] = {
        }

    def _draw_string(self, string: str, x: int, y: int):
        for index, letter in enumerate(string.upper()):
            if letter in [' ', ':', '.']:
                continue
            new_x = x + index * self.spritesheet.spritesheet_config.tile_size * self.zoom
            self.spritesheet.copy_tile_into_buffer(
                self.layer.buffer_view,
                letter,
                Rotation.R0,
                new_x,
                y * self.spritesheet.spritesheet_config.tile_size * self.zoom,
                self.zoom, 
                0
            )

    def _update_values(self):
        for key, (get_value, x ,y) in self.game_values.items():
            value = get_value()
            # if value == self.game_values[key]:
            #     continue
            self.game_values[key] = (get_value, x ,y)
            # else:
            self._draw_string(f"{key}: {value}", x, y)

    # def _draw_time(self):
    #     left_time = self.last_hud_info.get("time")
    #     if left_time is not None:
    #         if left_time == self.game_state.level_time_left:
    #             return
    #         else:
    #             self._draw_string(f"time left: {self.game_state.level_time_left}", 0, 0)
    #     else:
    #         self.last_hud_info["time"] = self.game_state.level_time_left

    # def _draw_lives(self):
    #     left_time = self.last_hud_info.get("lives")
    #     if left_time is not None:
    #         if left_time == self.game_state.lives:
    #             return
    #         else:
    #             self._draw_string(f"lives left: {self.game_state.lives}", 0, 1)
    #     else:
    #         self.last_hud_info["lives"] = self.game_state.lives

    # def _draw_level_info(self):
    #     left_time = self.last_hud_info.get("level")
    #     if left_time is not None:
    #         if left_time == self.game_state.level:
    #             return
    #         else:
    #             self._draw_string(f"level: {self.game_state.level}", 0, 2)
    #     else:
    #         self.last_hud_info["level"] = self.game_state.level

    # def _draw_score(self):
    #     left_time = self.last_hud_info.get("score")
    #     if left_time is not None:
    #         if left_time == self.game_state.score:
    #             return
    #         else:
    #             self._draw_string(f"score: {self.game_state.score}", 0, 3)
    #     else:
    #         self.last_hud_info["score"] = self.game_state.score

    def update_hud(self, dt):
        self.layer.clear()
        # self._draw_time()
        self._update_values()