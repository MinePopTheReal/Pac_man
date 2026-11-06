from src.game_state.game_state import GameState
from src.parsing.models import GameConfig


class Session:
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.game_state = GameState(config)

    def new_game(self) -> None:
        self.game_state = GameState(self.config)
