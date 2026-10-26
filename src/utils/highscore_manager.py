from src.utils.file_manager import FileManager
from src.parsing.models import GameConfig
from src.message.warning import WarningMessage
from src.message.errors import Error
import json

MAX_SCORES = 10

MAX_NAME_LENGTH = 10


class HighscoreManager:
    def __init__(self, config: GameConfig) -> None:
        self.path_file = config.highscore_filename
        self.lst_scores: list[tuple[str, int]] = []

    def load_highscores(self) -> None:
        try:
            content = FileManager.read(self.path_file)
        except Error:
            print(WarningMessage("No highscore file, "
                                 "starting with an empty list"))
            return

        try:
            lst_content = json.loads(content)
        except json.JSONDecodeError:
            print(WarningMessage("Highscore file is not valid JSON, "
                                 "starting with an empty list"))
            return

        if not isinstance(lst_content, list):
            print(WarningMessage("Highscore file must contain a list,"
                                 "starting with an empty list"))
            return

        for element in lst_content:
            if not isinstance(element, dict):
                print(WarningMessage("Invalid highscore entry ignored"))
                continue
            name = element.get('name')
            score = element.get('score')

            if (not isinstance(name, str) or not isinstance(score, int)
               or isinstance(score, bool)):
                continue

            self.add_name_score(name, score)

    def add_name_score(self, name: str, score: int) -> None:
        if not self.is_valid_name(name) or score < 0:
            return

        self.lst_scores.append((name.strip(), score))
        self.lst_scores = sorted(self.lst_scores, key=lambda x: x[1],
                                 reverse=True)[:MAX_SCORES]

    def save_highscores(self) -> None:
        lst_dict: list[dict[str, int | str]] = [
            {'name': name, 'score': score} for name, score in self.lst_scores]
        try:
            FileManager.write(lst_dict, self.path_file)
        except Error:
            print(WarningMessage("Could not save the highscores"))

    @staticmethod
    def is_valid_name(name: str) -> bool:
        if not 1 <= len(name.strip()) <= MAX_NAME_LENGTH:
            return False

        for char in name:
            if not (char.isalnum() or char == " "):
                return False
        return True
