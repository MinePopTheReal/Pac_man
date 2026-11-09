from enum import Enum
from abc import ABC


class Direction(Enum):
    """
    Simple Enum for Directions
    """
    NONE = (0, 0)
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Character(ABC):
    def __init__(
        self, direction: Direction, position: tuple[float, float], speed: float
    ) -> None:
        """initialization class character.
        Args:
            position (tuple[float, float]): Cell: (y, x) row, column
            direction (Direction): character direction(UP, DOWN, LEFT, RIGHT)
            speed (float): character speed
        """
        self.position = position
        self.direction = direction
        self.speed = speed

    def move(self, dt: float) -> None:
        """The logic for frame-by-frame movement allows the
        character's new position to be calculated

        Args:
            dt (float): new position
        """
        y, x = self.position
        dir_y, dir_x = self.direction.value
        distance = self.speed * dt
        new_pos_y = y + dir_y * distance
        new_pos_x = x + dir_x * distance
        self.position = (new_pos_y, new_pos_x)
