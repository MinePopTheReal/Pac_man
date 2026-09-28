from json import loads, JSONDecodeError
from re import sub, escape, DOTALL
from pydantic import BaseModel
from typing import TypeVar

from src.utils.file_manager import FileManager
from src.message.errors import ParsingError


class ConfigParser:
    """
    Parser for json config
    """    

    T = TypeVar('T', bound=BaseModel)

    def __init__(self) -> None:
        self.single_line_comment_markers = ["#", "//"]
        self.multi_line_comment_markers = [("/*", "*/")]

    def _remove_comment(self, file_content: str) -> str:
        """
        Remove comment from file content

        Args:
            file_content (str): content of the file

        Returns:
            str: Return the contents of the file without the comments
        """        
        text = file_content
        for start_marker, end_maker in self.multi_line_comment_markers:
            pattern = rf"{escape(start_marker)}.*?{escape(end_maker)}"
            text = sub(pattern, "", text, flags=DOTALL)
        for single_marker in self.single_line_comment_markers:
            text = sub(rf"{single_marker}.*", "", text)
        for start_marker, end_maker in self.multi_line_comment_markers:
            if start_marker in text or end_maker in text:
                raise ParsingError("Missing comment marker")
        return text

    def load_config(self, path: str, return_type: type[T]) -> type[T]:
        """
        load, clean and create obj 

        Args:
            path (str): path to the onfig file
            return_type (type[T]): pydantic model for the return 

        Returns:
            type[T]: config into pydantic model
        """        
        file_content = FileManager.read(path)

        clean_file_Content = self._remove_comment(file_content)
        try:
            file_datas = loads(clean_file_Content)
        except JSONDecodeError as e:
            raise ParsingError("An error occurred while loading the file")

        obj = return_type(**file_datas)
        return obj
