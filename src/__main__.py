from src.screen_manager.screen_manager import ScreenManager
from src.screen_manager.instructions_screen import Instructions
from src.rendering.assets import Assets, ACTUAL_RESOLUTION
from src.screen_manager.high_score_screen import HighScore
from src.utils.high_score_manager import HighScoreManager
from src.screen_manager.pause_screen import Pause
from src.parsing.parse_config import ConfigParser
from src.screen_manager.main_menu import MainMenu
from src.game_state.game_state import GameConfig
from src.screen_manager.game_screen import Play
from src.screen_manager.end_game import EndGame
from src.game_state.session import Session
from src.rendering.display import Display
from src.message.errors import Error
from src.screen_manager.screen import ScreenName


from pyglet import app


def main() -> None:
    config = ConfigParser().load_config("config.json", GameConfig)

    screen_manager = ScreenManager()
    Display(screen_manager)

    assets = Assets(ACTUAL_RESOLUTION[0], ACTUAL_RESOLUTION[1])

    high_score_manager = HighScoreManager(config)
    high_score_manager.load_high_score()

    session = Session(config)

    rs = screen_manager.register_screens
    rs(ScreenName.MAIN, MainMenu(config, screen_manager, assets))
    rs(ScreenName.PLAY, Play(
        session,
        screen_manager,
        assets,
        high_score_manager
    ))
    rs(ScreenName.INSTRUCTION, Instructions(screen_manager, assets))
    rs(ScreenName.HIGHSCORE, HighScore(
        config,
        screen_manager,
        high_score_manager,
        assets
    ))
    rs(ScreenName.PAUSE, Pause(screen_manager, session, assets))
    rs(ScreenName.ENDGAME, EndGame(
        session,
        screen_manager,
        high_score_manager,
        assets
    ))

    screen_manager.first_screen(ScreenName.MAIN)

    app.run()


if __name__ == "__main__":
    try:
        main()
    except Error as e:
        print(e)
    except KeyboardInterrupt:
        print(Error("You have stopped the program"))
