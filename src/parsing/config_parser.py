from src.utils.file_manager import FileManager
from src.message.errors import ParsingError


from json import loads, JSONDecodeError
from pydantic import BaseModel
from typing import TypeVar


class ConfigParser:
    """
    Parser for json config
    """

    T = TypeVar("T", bound=BaseModel)

    def __init__(self) -> None:
        self.comment_markers = [("/*", "*/"), ("#", None), ("//", None)]

    @staticmethod
    def _is_in_string(text: str, curr_state: bool, i: int) -> bool:
        """
        checks whether the cursor is within a string

        Args:
            text (str): the text we want to check
            curr_state (bool): whether we're already in a string or not
            i (int): the benchmark against which to reassess

        Returns:
            bool: whether or not we are in a string
        """
        in_string = curr_state
        if text[i] == '"':
            nb_escape = 0
            j = i - 1

            while j >= 0 and text[j] == "\\":
                nb_escape += 1
                j -= 1

            if nb_escape % 2 == 0:
                in_string = not in_string
        return in_string

    def _check_comment_traces(self, text: str) -> None:
        """
        Checks to see if there are any comments that have been
        closed but not opened

        Args:
            text (str): the text we want to check
        """
        i = 0
        in_string = False
        while i < len(text):
            in_string = self._is_in_string(text, in_string, i)

            if not in_string:
                for _, end_marker in self.comment_markers:
                    if end_marker is not None and text.startswith(
                        end_marker, i
                    ):
                        raise ParsingError("Missing comment marker")
            i += 1

    def _remove_comment(self, file_content: str) -> str:
        """
        Remove comment from file content

        Args:
            file_content (str): content of the file

        Returns:
            str: Return the contents of the file without the comments
        """
        i = 0
        text = file_content
        in_string = False

        while i < len(text):
            in_string = self._is_in_string(text, in_string, i)

            if not in_string:

                for start_marker, end_marker in self.comment_markers:
                    if text.startswith(start_marker, i):
                        start = i
                        end = -1
                        while i <= len(text):
                            if end_marker is None:
                                is_end = i == len(text) or text[
                                    start:i
                                ].endswith("\n")
                            else:
                                is_end = i - start >= len(start_marker) + len(
                                    end_marker
                                ) and text[start:i].endswith(end_marker)
                            if is_end:
                                end = i
                                break
                            i += 1
                        if end == -1:
                            raise ParsingError("Missing comment marker")
                        text = text[:start] + text[end:]
                        i = start - 1
            i += 1

        self._check_comment_traces(text)
        return text

    def load_config(self, path: str, return_type: type[T]) -> T:
        """
        load, clean and create obj

        Args:
            path (str): path to the config file
            return_type (type[T]): pydantic model for the return

        Returns:
            type[T]: config into pydantic model
        """
        file_content = FileManager.read(path)

        clean_file_Content = self._remove_comment(file_content)
        try:
            file_datas = loads(clean_file_Content)
        except JSONDecodeError as e:
            raise ParsingError(
                "An error occurred while loading the file"
            ) from e

        if not isinstance(file_datas, dict):
            raise ParsingError(
                "Invalid configuration file format. Key-value "
                "pairs are expected in the following format: key:value"
            )

        obj = return_type(**file_datas)
        return obj
