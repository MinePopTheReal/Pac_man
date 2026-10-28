from src.game_state.game_state import GameState, GameConfig
from src.screen_manager.screen_manager import ScreenManager
from src.parsing.parse_config import ConfigParser
from src.screen_manager.main_menu import MainMenu
from src.screen_manager.game_screen import Play
from src.screen_manager.highscores_screen import Highscore
from src.rendering.display import Display
from src.rendering.assets import Assets
from src.utils.highscore_manager import HighscoreManager
from src.screen_manager.instructions_screen import Instructions

from pyglet import app


config = ConfigParser().load_config("config.json", GameConfig)

screen_manager = ScreenManager()

render = Display(screen_manager)
assets = Assets(render.screen.width, render.screen.height, render.width,
                render.height)

high_score_manager = HighscoreManager(config)

high_score_manager.load_highscores()

play_screen = Play(screen_manager, config, assets, high_score_manager)
highscores_screen = Highscore(screen_manager, high_score_manager, assets,
                              config)
instructions_screen = Instructions(screen_manager, assets)
main = MainMenu(screen_manager, config, assets, high_score_manager,
                instructions_screen, play_screen, highscores_screen)


# screen_manager.push(play)
screen_manager.first_screen(main)

app.run()
