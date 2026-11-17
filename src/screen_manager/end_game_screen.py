from src.rendering.widget.input_field import InputField, MAX_NAME_LENGTH
from src.utils.high_score_manager import HighScoreManager
from src.screen_manager.screen import Screen, Navigator
from src.rendering.widget.label import Label
from src.game.game_state import GameStatus
from src.game.session import Session
from src.rendering.assets import (
    Assets,
    H3_PX_SIZE,
    H1_PX_SIZE,
    MINOR_COLOR,
    MAJOR_COLOR,
    SCALE_FACTOR,
)


from pyglet.window import key as keys


class EndGameScreen(Screen):
    """Screen shown at the end of a game, after a victory or a defeat.

    It displays the final score and the best score, and lets the player
    type a name to save the score in the high score list.
    """
    def __init__(
        self,
        navigator: Navigator,
        high_score_manager: HighScoreManager,
        session: Session,
        assets: Assets,
    ) -> None:
        super().__init__(navigator, assets)
        self.high_score_manager = high_score_manager
        self.session = session

    def build_widget(self) -> None:
        """Build the widgets and clear the name typed by the player.

        Called each time the screen is shown. The title depends on the
        result of the game (victory or game over).
        """
        self.prompt = "Enter your username:"
        self.name: str = ""
        self.empty: str = "_" * MAX_NAME_LENGTH

        self.title = Label(
            "victory"
            if self.session.game_state.status == GameStatus.WON
            else "game over",
            H1_PX_SIZE,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(self.assets.window_height - 200 * SCALE_FACTOR),
            anchor_x=0.5,
            anchor_y=1,
        )

        title_bottom = self.title.y - self.title.height
        your_score = self.session.game_state.score
        self.your_score_label = Label(
            f"your score: {your_score}",
            H3_PX_SIZE,
            self.assets.font_spritesheet,
            MINOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(title_bottom - 500 * SCALE_FACTOR),
            anchor_x=0.5,
            anchor_y=0,
        )

        your_score_bottom = (
            self.your_score_label.y - self.your_score_label.height
        )

        best_score = your_score
        if len(self.high_score_manager.lst_scores) > 0:
            best_score = self.high_score_manager.lst_scores[0][1]
        self.best_score_label = Label(
            f"best score: {best_score}",
            H3_PX_SIZE,
            self.assets.font_spritesheet,
            MINOR_COLOR,
            x=self.assets.window_width // 2,
            y=your_score_bottom - H3_PX_SIZE // 2,
            anchor_x=0.5,
            anchor_y=0,
        )

        best_score_bottom = (
            self.best_score_label.y - self.best_score_label.height
        )
        self.input_field = InputField(
            self.prompt,
            H3_PX_SIZE,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            MINOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(best_score_bottom - 100 * SCALE_FACTOR),
            anchor_x=0.5,
            anchor_y=1,
        )
        self._refresh_input()

    def input(self, key: int) -> None:
        """Handle a key pressed while the player types a name.

        Letters, digits and space add a character (up to the maximum
        length), Backspace removes the last one, Enter saves the score,
        and Escape leaves without saving it.

        Args:
            key (int): The code of the key (see pyglet.window.key).
        """
        if (
            keys.A <= key <= keys.Z
            or keys._0 <= key <= keys._9
            or key == keys.SPACE
        ):

            if len(self.name) < MAX_NAME_LENGTH:
                self.name += chr(key).upper()
                self.empty = self.empty[:-1]
                self._refresh_input()

        elif key == keys.BACKSPACE:
            self.name = self.name[:-1]
            if len(self.empty) < MAX_NAME_LENGTH:
                self.empty += "_"
                self._refresh_input()

        elif key == keys.ENTER:
            self._validate()

        elif key == keys.ESCAPE:
            self.session.new_game()
            self.navigator.back_to_menu()

    def _refresh_input(self) -> None:
        """Redraw the input field with the name and the empty slots."""
        self.input_field.set_text(self.name + self.empty)

    def _validate(self) -> None:
        """Save the score under the typed name and go back to the menu.

        Does nothing if the name is not valid (empty, too long or with
        forbidden characters), so the player can correct it.
        """
        if not self.high_score_manager.is_valid_name(self.name):
            return
        self.high_score_manager.add_name_score(
            self.name, self.session.game_state.score
        )
        self.session.new_game()
        self.high_score_manager.save_high_score()
        self.navigator.back_to_menu()

    def draw_screen(self) -> None:
        """Draw the title, the scores and the input field."""
        self.title.draw()
        self.your_score_label.draw()
        self.best_score_label.draw()
        self.input_field.draw()
