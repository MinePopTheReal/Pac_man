from src.utils.widget.input_field import MAX_NAME_LENGTH
from src.message.warning import WarningMessage
from src.utils.file_manager import FileManager
from src.parsing.models import GameConfig
from src.message.errors import Error


import json


MAX_HIGHSCORE = 10


class HighScoreManager:
    def __init__(self, config: GameConfig) -> None:
        self.path_file = config.high_score_filename
        self.lst_scores: list[tuple[str, int]] = []

    def load_high_score(self) -> None:
        try:
            content = FileManager.read(self.path_file)
        except Error:
            print(
                WarningMessage(
                    "No high score file, " "starting with an empty list"
                )
            )
            return

        try:
            lst_content = json.loads(content)
        except json.JSONDecodeError:
            print(
                WarningMessage(
                    "High score file is not valid JSON, "
                    "starting with an empty list"
                )
            )
            return

        if not isinstance(lst_content, list):
            print(
                WarningMessage(
                    "High score file must contain a list,"
                    "starting with an empty list"
                )
            )
            return

        for element in lst_content:
            if not isinstance(element, dict):
                print(WarningMessage("Invalid high score entry ignored"))
                continue
            name = element.get("name")
            score = element.get("score")

            if (
                not isinstance(name, str)
                or not isinstance(score, int)
                or isinstance(score, bool)
            ):
                continue

            self.add_name_score(name, score)

    def add_name_score(self, name: str, score: int) -> None:
        if not self.is_valid_name(name) or score < 0:
            return

        self.lst_scores.append((name.strip(), score))
        self.lst_scores = sorted(
            self.lst_scores, key=lambda x: x[1], reverse=True
        )[:MAX_HIGHSCORE]

    def save_high_score(self) -> None:
        lst_dict: list[dict[str, int | str]] = [
            {"name": name, "score": score} for name, score in self.lst_scores
        ]
        try:
            FileManager.write(lst_dict, self.path_file)
        except Error:
            print(WarningMessage("Could not save the high_score"))

    @staticmethod
    def is_valid_name(name: str) -> bool:
        if not 1 <= len(name.strip()) <= MAX_NAME_LENGTH:
            return False

        for char in name:
            if not (char.isalnum() or char == " "):
                return False
        return True
