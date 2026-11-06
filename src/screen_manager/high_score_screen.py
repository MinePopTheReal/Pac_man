from src.utils.widget.high_score_label import HighScoresLabel
from src.utils.high_score_manager import HighScoreManager
from src.screen_manager.screen import Screen, Navigator
from src.parsing.models import GameConfig
from src.utils.widget.label import Label
from src.rendering.assets import Assets
from src.rendering.assets import (
    H1_PX_SIZE,
    H3_PX_SIZE,
    MAJOR_COLOR,
    MINOR_COLOR,
    TOP1_COLOR,
    TOP2_COLOR,
    TOP3_COLOR,
    SCALE_FACTOR,
)


from pyglet.window import key as keys


class HighScore(Screen):
    TITLE = "HIGHSCORE"

    def __init__(
        self,
        config: GameConfig,
        navigator: Navigator,
        high_score: HighScoreManager,
        assets: Assets,
    ) -> None:
        super().__init__(navigator, assets)
        self.high_score = high_score
        self.config = config

        self.set_screens()

    def input(self, key: int) -> None:
        if key in (keys.ESCAPE, keys.ENTER):
            self.navigator.pop()

    def set_screens(self) -> None:
        self.title = Label(
            self.TITLE,
            H1_PX_SIZE,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(self.assets.window_height - 200 * SCALE_FACTOR),
            anchor_x=0.5,
            anchor_y=1,
        )

        title_bottom = self.title.y - self.title.height
        self.high_score_label = HighScoresLabel(
            H3_PX_SIZE,
            self.assets.font_spritesheet,
            TOP1_COLOR,
            TOP2_COLOR,
            TOP3_COLOR,
            MINOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(title_bottom - 200 * SCALE_FACTOR),
            anchor_x=0.5,
            anchor_y=1,
        )

    def draw_screen(self) -> None:
        self.title.draw()
        self.high_score_label.set_scores(self.high_score.lst_scores)
        self.high_score_label.draw()
