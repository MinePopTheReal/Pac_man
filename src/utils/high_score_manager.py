from src.message.warning_message import WarningMessage
from src.utils.file_manager import FileManager
from src.parsing.models import GameConfig
from src.game.game_state import MAX_SCORE
from src.message.errors import Error
from src.utils.paths import app_dir


from json import loads, JSONDecodeError


MAX_HIGH_SCORE = 10
MAX_NAME_LENGTH = 10


class HighScoreManager:
    """Keeps the list of the best scores and saves it in a JSON file.

    The list holds at most MAX_HIGH_SCORE (name, score) pairs, from the
    best to the worst. It is read from the file with load_high_score(),
    changed with add_name_score(), and written back with
    save_high_score(). A problem with the file never stops the game:
    a warning is printed and the list is simply left empty.
    """
    def __init__(self, config: GameConfig) -> None:
        self.path_file = str(app_dir() / config.high_score_filename)
        self.lst_scores: list[tuple[str, int]] = []

    def load_high_score(self) -> None:
        """Read the scores from the file and add them to the list.

        The file must contain a JSON list of objects with a "name" and a
        "score". If the file is missing, is not valid JSON, or does not
        contain a list, a warning is printed and nothing is loaded. An
        entry that is not valid (wrong type, invalid name, negative or above
        score) is ignored, and the other entries are still loaded. Only
        the best MAX_HIGH_SCORE scores are kept.

        The scores are added to the list, not put in place of it: calling
        this method twice adds the scores twice.
        """
        try:
            content = FileManager.read(self.path_file)
        except Error:
            print(
                WarningMessage(
                    "No high score file, "
                    "starting with an empty list"
                )
            )
            return

        try:
            lst_content = loads(content)
        except JSONDecodeError:
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
                    "High score file must contain a list, "
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
        """Add a score to the list, if it is valid.

        Does nothing if the name is not valid or the score is negative
        or above MAX_SCORE.
        Otherwise the list is sorted again from the best score to the
        worst and cut to MAX_HIGH_SCORE entries, so a score that is too
        low for the list is dropped. When two scores are equal, the one
        added first stays first. The spaces around the name are removed.

        The file is not changed: call save_high_score() for that.

        Args:
            name (str): The name of the player.
            score (int): The score, which must not be negative
                          or above MAX_SCORE.
        """
        if not self.is_valid_name(name) or not (0 <= score <= MAX_SCORE):
            return

        self.lst_scores.append((name.strip(), score))
        self.lst_scores = sorted(
            self.lst_scores, key=lambda x: x[1], reverse=True
        )[:MAX_HIGH_SCORE]

    def save_high_score(self) -> None:
        """Write the list of scores in the high score file.

        The file is created, with its folders, if it does not exist. If
        it cannot be written, a warning is printed and the game goes on.
        """
        lst_dict: list[dict[str, int | str]] = [
            {"name": name, "score": score} for name, score in self.lst_scores
        ]
        try:
            FileManager.write(lst_dict, self.path_file)
        except Error:
            print(WarningMessage("Could not save the high_score"))

    @staticmethod
    def is_valid_name(name: str) -> bool:
        """Tell if a name can be used in the high score list.

        A valid name has between 1 and MAX_NAME_LENGTH characters, not
        counting the spaces around it, and is made only of letters,
        digits and spaces.

        Args:
            name (str): The name to check.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        if not 1 <= len(name.strip()) <= MAX_NAME_LENGTH:
            return False

        for char in name:
            if not (char.isalnum() or char == " "):
                return False
        return True
