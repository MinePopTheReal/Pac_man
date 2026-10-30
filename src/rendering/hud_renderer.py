from src.utils.sprite_sheet_manager import SpriteSheetManager
from src.rendering.assets import HUD_ZOOM, MAJOR_COLOR
from src.utils.text_renderer import TextRenderer
from src.game_state.game_state import GameState
from src.rendering.layer import Layer


MAX_SCORE_LENGHT = 10


class HudRenderer:
    """
    HUD rendering and management
    """    
    def __init__(
        self,
        game_state: GameState,
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
            "level": (self._get_level, 15, 0),
            "score": (lambda: min(int(self._get_score()), (10**MAX_SCORE_LENGHT - 1)), 15, 1)
        }
    def _get_time(self) -> str:
        """Create a string representation of the remaining time

        Returns:
            str: the remaining time as a string
        """        
        time = int(self.game_state.level_time_left)
        string = f"{time // 60}m {time % 60}s"
        return string

    def _get_lives(self) -> str:
        """Create a string representation of the remaining lives

        Returns:
            str: the remaining lives as a string
        """        
        return (
            f"{"❤" * min(self.game_state.lives, 3)}"
            f"{"+" if self.game_state.lives > 3 else ""}"
            )

    def _get_level(self) -> str:
        """Create the string that represents the current level 

        Returns:
            str: the level as a string
        """        
        return f"{self.game_state.level}"

    def _get_score(self) -> str:
        """Create the string that represents the current score 

        Returns:
            str: the score as a string
        """        
        return f"{self.game_state.score}"

    def update_hud(self, dt: float) -> None:
        """Updates all HUD values

        Args:
            dt (float): Delta time, which is not used but is required
        """        
        self.layer.clear()
        for key, (get_value, x, y) in self.game_values.items():
            value = get_value()
            TextRenderer.draw_string(
                self.layer.buffer_view,
                f"{key + ':':<6}{value}",
                x,
                y,
                HUD_ZOOM,
                self.spritesheet,
                MAJOR_COLOR
            )
