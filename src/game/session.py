from src.game.game_state import GameState
from src.parsing.models import GameConfig


class Session:
    """
    Stores information about the current game and makes
    it easy to start a new game
    """
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.game_state = GameState(config)

    def new_game(self) -> None:
        """
        allows you to generate a new maze that's ready to play
        """
        self.game_state = GameState(self.config)
