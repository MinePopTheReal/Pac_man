from abc import ABC
from enum import Enum


class Direction(Enum):
    NONE = (0, 0)
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Character(ABC):
    def __init__(self, direction: Direction,
                 position: tuple[float, float], speed: float) -> None:
        """initialization class character.
                Args:
                    position (tuple[float, float]): Cell: (y, x) row, column
                    state (str): Character's state.
                    direction (str): character direction(UP, DOWN, LEFT, RIGHT)
                """
        self.position = position
        self.direction = direction
        self.speed = speed

    def movement(self, dt: float) -> None:
        y, x = self.position
        dir_y, dir_x = self.direction.value
        distance = self.speed * dt
        new_pos_y = y + dir_y * distance
        new_pos_x = x + dir_x * distance
        self.position = (new_pos_y, new_pos_x)
