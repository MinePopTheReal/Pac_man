from src.screen_manager.screen import Screen, Navigator
from src.utils.widget.label import Label
from src.rendering.assets import (
    Assets,
    H1_PX_SIZE,
    H4_PX_SIZE,
    H5_PX_SIZE,
    SCALE_FACTOR,
    MINOR_COLOR,
    MAJOR_COLOR,
)


from pyglet.window import key as keys


class Instructions(Screen):
    TITLE = "instructions"

    def __init__(
        self,
        navigator: Navigator,
        assets: Assets
    ) -> None:
        """Screen that explains the rules and the controls of the game.

        The texts are fixed. The player leaves the screen with Escape or
        Enter.
        """
        super().__init__(navigator, assets)
        self.rules: str = (
            "EAT ALL THE PACGUMS TO\n"
            "CLEAR THE LEVEL.\n\n"
            "AVOID THE 4 GHOSTS.\n"
            "IF ONE TOUCHES YOU\n"
            "YOU LOSE A LIFE.\n\n"
            "SUPER PACGUMS MAKE GHOSTS\n"
            "VULNERABLE FOR A FEW SECONDS\n"
            "EAT THEM FOR BONUS POINTS.\n\n"
            "NO LIVES LEFT:\n"
            "GAME OVER\n\n"
            "GET THE BEST SCORE.\n"
        )

        self.controls: str = (
            "GAME:\n"
            "MOVE: WASD OR ARROWS\n"
            "ESC: PAUSE\n"
            "\nMENUS:\n"
            "MOVE: W S OR UP DOWN\n"
            "ENTER: VALIDATE\n"
            "ESC: GO BACK\n"
            "\nCHEATS:\n"
            "C: TOGGLE CHEATS\n"
            "THEN PICK WITH 1 TO 6\n\n"
            "1: INVINCIBLE\n"
            "2: FREEZE GHOSTS\n"
            "3: SKIP LEVEL\n"
            "4: EXTRA LIFE\n"
            "5: FAST PACMAN\n"
            "6: SLOW GHOSTS\n"
        )

    def input(self, key: int) -> None:
        """Go back to the previous screen when Escape or Enter is pressed.

        Other keys are ignored.

        Args:
            key (int): The code of the key (see pyglet.window.key).
        """
        if key in (keys.ESCAPE, keys.ENTER):
            self.navigator.pop()

    def set_screens(self) -> None:
        """Build the labels of the screen.

        Called when the screen is created and each time it is shown.
        The title, the rules and the controls are stacked from top to
        bottom, each one placed under the previous one.
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
        self.sub_title_rules = Label(
            "rules",
            H4_PX_SIZE,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(title_bottom - 150 * SCALE_FACTOR),
            anchor_x=0.5,
            anchor_y=1,
        )

        sub_title_rules_bottom = (
            self.sub_title_rules.y - self.sub_title_rules.height
        )
        self.rules_label = Label(
            self.rules,
            H5_PX_SIZE,
            self.assets.font_spritesheet,
            MINOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(sub_title_rules_bottom - 20 * SCALE_FACTOR),
            anchor_x=0.5,
            anchor_y=1,
        )

        rules_bottom = self.rules_label.y - self.rules_label.height
        self.sub_title_controls = Label(
            "controls",
            H4_PX_SIZE,
            self.assets.font_spritesheet,
            MAJOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(rules_bottom - 50 * SCALE_FACTOR),
            anchor_x=0.5,
            anchor_y=1,
        )

        sub_title_controls_bottom = (
            self.sub_title_controls.y - self.sub_title_controls.height
        )
        self.controls_label = Label(
            self.controls,
            H5_PX_SIZE,
            self.assets.font_spritesheet,
            MINOR_COLOR,
            x=self.assets.window_width // 2,
            y=int(sub_title_controls_bottom - 20 * SCALE_FACTOR),
            anchor_x=0.5,
            anchor_y=1,
            align="left",
        )

    def draw_screen(self) -> None:
        """Draw the title, the rules and the controls."""
        self.title.draw()
        self.sub_title_rules.draw()
        self.sub_title_controls.draw()
        self.controls_label.draw()
        self.rules_label.draw()
