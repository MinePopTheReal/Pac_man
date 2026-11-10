from src.rendering.widget.high_score_label import HighScoreLabel
from src.utils.high_score_manager import HighScoreManager
from src.screen_manager.screen import Screen, Navigator
from src.rendering.widget.label import Label
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


class HighScoreScreen(Screen):
    """Screen that shows the list of the best scores.

    The scores come from the high score manager. The first three are
    drawn with their own color. The player leaves the screen with
    Escape or Enter.
    """
    TITLE = "HIGH_SCORE"

    def __init__(
        self,
        navigator: Navigator,
        high_score: HighScoreManager,
        assets: Assets,
    ) -> None:
        super().__init__(navigator, assets)
        self.high_score = high_score

    def input(self, key: int) -> None:
        """Go back to the previous screen when Escape or Enter is pressed.

        Other keys are ignored.

        Args:
            key (int): The code of the key (see pyglet.window.key).
        """
        if key in (keys.ESCAPE, keys.ENTER):
            self.navigator.pop()

    def build_widget(self) -> None:
        """Build the title and the score list widgets.

        Called when the screen is created and each time it is shown.
        The score list is placed under the title and is centered
        horizontally.
        """
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
        self.high_score_label = HighScoreLabel(
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
        """Draw the title and the high score list.

        The list is given the current scores before being drawn, so a
        score added since the last time is displayed. The label redraws
        its content only when the scores have changed.
        """
        self.title.draw()
        self.high_score_label.set_scores(self.high_score.lst_scores)
        self.high_score_label.draw()
