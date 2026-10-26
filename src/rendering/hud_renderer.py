from src.rendering.layer import Layer
from src.utils.sprite_sheet_manager import SpriteSheetManager, Rotation
from src.game_state.game_state import GameState


class HudRenderer:
    def __init__(
        self, game_state: GameState,
        spritesheet: SpriteSheetManager,
        layer: Layer,
        zoom: int
    ):
        self.game_state: GameState = game_state
        self.spritesheet: SpriteSheetManager = spritesheet
        self.layer: Layer = layer
        self.zoom = zoom

        self.game_values = {
            "time": (self._get_time, 0, 0),
            "lives": (self._get_lives, 0, 1),
            "level": (self._get_level, 20, 0),
            "score": (self._get_score, 20, 1)
        }

    def _draw_string(self, string: str, x: int, y: int) -> None:
        for index, letter in enumerate(string.upper()):
            if letter in [' ']:
                continue
            new_x = (x + index) \
                * self.spritesheet.spritesheet_config.tile_size \
                * self.zoom
            self.spritesheet.copy_tile_into_buffer(
                self.layer.buffer_view,
                letter,
                Rotation.R0,
                new_x,
                y * self.spritesheet.spritesheet_config.tile_size * self.zoom,
                self.zoom,
                0
            )

    def _get_time(self) -> str:
        time = int(self.game_state.level_time_left)
        string = f"{time // 60}m {time % 60}s"
        return string

    def _get_lives(self) -> str:
        return (
            f"{"❤" * min(self.game_state.lives, 3)}"
            f"{"+" if self.game_state.lives > 3 else ""}"
            )

    def _get_level(self) -> str:
        return f"{self.game_state.level}"

    def _get_score(self) -> str:
        return f"{self.game_state.score}"

    def _update_values(self) -> None:
        for key, (get_value, x, y) in self.game_values.items():
            value = get_value()
            self._draw_string(f"{key + ':':<6}{value}", x, y)

    def update_hud(self, dt: float) -> None:
        self.layer.clear()
        self._update_values()
