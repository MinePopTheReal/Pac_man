from src.message.errors import Error
from pathlib import Path
from typing import Any
from json import dump


class FileManager:
    """
    makes it easier to manage files
    """
    @staticmethod
    def read(file_path: str) -> str:
        """
        allows you to read a file

        Args:
            file_path (str): the file path

        Returns:
            str: the contents of the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                data = f.read()

            return data
        except IsADirectoryError as e:
            raise Error(
                f"The path points to a folder: {file_path}"
            ) from e

        except FileNotFoundError as e:
            raise Error(
                f"File not found: {file_path}"
            ) from e

        except PermissionError as e:
            raise Error(
                f"Permission denied: {file_path}"
            ) from e

        except OSError as e:
            raise Error(
                f"Unable to read file: {file_path}"
            ) from e

    @staticmethod
    def write(obj: Any, file_path: str) -> None:
        """
        allows you to write to and create a json file
        if it doesn't already exist

        Args:
            obj (Any): A Python object that can be used as JSON
            file_path (str): the file path
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding="utf-8") as f:
                dump(obj, f, indent=4, ensure_ascii=False)

        except IsADirectoryError as e:
            raise Error(
                f"The path points to a folder: {file_path}"
            ) from e

        except FileNotFoundError as e:
            raise Error(
                f"File not found: {file_path}"
            ) from e

        except PermissionError as e:
            raise Error(
                f"Permission denied: {file_path}"
            ) from e

        except UnicodeEncodeError as e:
            raise Error(
                "Error when encode"
            ) from e

        except TypeError as e:
            raise Error(
                "Object is not JSON serializable"
            ) from e

        except OSError as e:
            raise Error(
                f"Unable to write file: {file_path}"
            ) from e
