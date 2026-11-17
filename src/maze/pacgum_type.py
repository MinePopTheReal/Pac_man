from enum import Enum, auto


class PacgumType(Enum):
    """What a cell of the maze can contain."""

    PACGUM = auto()
    SUPER_PACGUM = auto()
