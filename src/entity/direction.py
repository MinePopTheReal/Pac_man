from enum import Enum


class Direction(Enum):
    """
    Simple Enum for Directions
    """
    NONE = (0, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
