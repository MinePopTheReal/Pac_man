from src.game_state.game_state import GameState, GameConfig
from src.screen_manager.screen_manager import ScreenManager
from src.parsing.parse_config import ConfigParser
from src.screen_manager.main_menu import MainMenu
from src.screen_manager.game_screen import Play
from src.rendering.display import Display
from src.rendering.assets import Assets
from src.utils.highscore_manager import HighscoreManager

from pyglet import app


config = ConfigParser().load_config("config.json", GameConfig)

screen_manager = ScreenManager()

render = Display(screen_manager)
assets = Assets(render.screen.width, render.screen.height, render.width, render.height)

high_score_manager = HighscoreManager(config)

high_score_manager.load_highscores()

main = MainMenu(config, screen_manager, assets, high_score_manager)
# play = Play(config, screen_manager, render)

# screen_manager.push(play)
screen_manager.first_screen(main)

app.run()
