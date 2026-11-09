from src.screen_manager.instructions_screen import Instructions
from src.screen_manager.screen_manager import ScreenManager
from src.rendering.assets import Assets, ACTUAL_RESOLUTION
from src.screen_manager.high_score_screen import HighScore
from src.utils.high_score_manager import HighScoreManager
from src.screen_manager.pause_screen import Pause
from src.parsing.parse_config import ConfigParser
from src.screen_manager.main_menu import MainMenu
from src.screen_manager.screen import ScreenName
from src.game_state.game_state import GameConfig
from src.screen_manager.game_screen import Play
from src.screen_manager.end_game import EndGame
from src.game_state.session import Session
from src.rendering.display import Display
from src.message.errors import Error

from argparse import ArgumentParser
from pyglet import app


def main() -> None:
    # TODO docstring
    # TODO norm
    """Build the game from a config file and run it.

    The path of the JSON config file is read from the command line.
    The function loads the config and the high scores, creates the
    window, the session and all the screens, shows the main menu, then
    starts the pyglet event loop. It returns when the window is closed
    or when the player quits from the menu.
    """

    parser = ArgumentParser(
        prog="pac-man.py", description="Pac-Man game."
    )

    parser.add_argument("config", help="path to the JSON config file")
    args = parser.parse_args()

    config = ConfigParser().load_config(args.config, GameConfig)

    screen_manager = ScreenManager()
    Display(screen_manager)

    assets = Assets(ACTUAL_RESOLUTION[0], ACTUAL_RESOLUTION[1])

    high_score_manager = HighScoreManager(config)
    high_score_manager.load_high_score()

    session = Session(config)

    rs = screen_manager.register_screens
    rs(ScreenName.MAIN, MainMenu(screen_manager, assets))
    rs(ScreenName.PLAY, Play(
        screen_manager,
        high_score_manager,
        session,
        assets
    ))
    rs(ScreenName.INSTRUCTION, Instructions(screen_manager, assets))
    rs(ScreenName.HIGH_SCORE, HighScore(
        screen_manager,
        high_score_manager,
        assets
    ))
    rs(ScreenName.PAUSE, Pause(screen_manager, session, assets))
    rs(ScreenName.ENDGAME, EndGame(
        screen_manager,
        high_score_manager,
        session,
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
