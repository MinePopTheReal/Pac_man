from src.utils.widget.input_field import InputField, MAX_NAME_LENGTH
from src.utils.high_score_manager import HighScoreManager
from src.screen_manager.screen import Screen, Navigator
from src.game_state.game_state import GameStatus
from src.game_state.session import Session
from src.utils.widget.label import Label
from src.rendering.assets import (
    Assets,
    H3_PX_SIZE,
    H1_PX_SIZE,
    MINOR_COLOR,
    MAJOR_COLOR,
    SCALE_FACTOR,
)


from pyglet.window import key as keys


class EndGame(Screen):
    def __init__(
        self,
        session: Session,
        navigator: Navigator,
        high_score_manager: HighScoreManager,
        assets: Assets,
    ) -> None:
        super().__init__(navigator, assets)
        self.high_score_manager = high_score_manager
        self.session = session

        self.set_screens()

    def set_screens(self) -> None:
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
            self.session.new_game()

        elif key == keys.ESCAPE:
            self.session.new_game()
            self.navigator.back_to_menu()

    def _refresh_input(self) -> None:
        self.input_field.set_text(self.name + self.empty)

    def _validate(self) -> None:
        if not self.high_score_manager.is_valid_name(self.name):
            return
        self.high_score_manager.add_name_score(
            self.name, self.session.game_state.score
        )
        self.high_score_manager.save_high_score()
        self.navigator.back_to_menu()

    def draw_screen(self) -> None:
        self.title.draw()
        self.your_score_label.draw()
        self.best_score_label.draw()
        self.input_field.draw()
