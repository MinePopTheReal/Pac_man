from src.message.colors import TerminalColors as TC


class Error(Exception):
    """
    The entire logic behind the creation of custom errors.
    """
    default_type = "Not defined"

    def __init__(
        self,
        message: str = "",
        type: str | None = None,
    ) -> None:
        self.message: str = message
        self.type: str = type or self.default_type

        super().__init__(message)

    def __str__(self) -> str:
        """
        Return the formatted error message.
        """
        return (
            f"{TC.BOLD}{TC.RED}[Error]{TC.END}: {self.message}"
            f"{' (' + self.type + ')' if self.type else ''}"
        )


class RenderError(Error):
    """Exception raised by the command line interface."""

    default_type = "Render"


class ParsingError(Error):
    """Exception raised by parser."""

    default_type = "Parsing"


class GridError(Error):
    """Exception raised when accessing a position outside the grid."""

    default_type = "Grid"

class ScreenError(Error):
    """Exception raised when the screen manager is
     used before first_screen()"""

    default_type = "Screen"


# add your own error