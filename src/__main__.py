from src.screen_manager.instructions_screen import InstructionsScreen
from src.screen_manager.high_score_screen import HighScoreScreen
from src.screen_manager.end_game_screen import EndGameScreen
from src.screen_manager.screen_manager import ScreenManager
from src.rendering.assets import Assets, compute_layout
from src.utils.high_score_manager import HighScoreManager
from src.screen_manager.pause_screen import PauseScreen
from src.screen_manager.game_screen import GameScreen
from src.screen_manager.main_screen import MainScreen
from src.parsing.config_parser import ConfigParser
from src.screen_manager.screen import ScreenName
from src.parsing.models import GameConfig
from src.rendering.display import Display
from src.game.session import Session
from src.message.errors import Error


from argparse import ArgumentParser
from pyglet import app


def main() -> None:
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
    layout = compute_layout()

    screen_manager = ScreenManager()
    Display(screen_manager, layout.width, layout.height)

    assets = Assets(layout)

    high_score_manager = HighScoreManager(config)
    high_score_manager.load_high_score()

    session = Session(config)

    rs = screen_manager.register_screens
    rs(ScreenName.MAIN, MainScreen(
        screen_manager, 
        assets,
        layout
    ))
    rs(ScreenName.GAME_SCREEN, GameScreen(
        screen_manager,
        high_score_manager,
        session,
        assets,
        layout
    ))
    rs(ScreenName.INSTRUCTIONS, InstructionsScreen(
        screen_manager, 
        assets,
        layout
    ))
    rs(ScreenName.HIGH_SCORE, HighScoreScreen(
        screen_manager,
        high_score_manager,
        assets,
        layout
    ))
    rs(ScreenName.PAUSE, PauseScreen(screen_manager, 
        session, 
        assets,
        layout
    ))
    rs(ScreenName.ENDGAME, EndGameScreen(
        screen_manager,
        high_score_manager,
        session,
        assets,
        layout
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
    # except Exception as e:
    #     print(Error(f"Unexpected error: {e}", f"{type(e).__name__}"))
