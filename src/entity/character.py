from src.entity.direction import Direction


from abc import ABC


class Character(ABC):
    def __init__(
        self, direction: Direction, position: tuple[float, float], speed: float
    ) -> None:
        """initialization class character.
        Args:
            position (tuple[float, float]): Cell: (x, y) row, column
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
        x, y = self.position
        dir_x, dir_y = self.direction.value
        distance = self.speed * dt
        new_pos_y = y + dir_y * distance
        new_pos_x = x + dir_x * distance
        self.position = (new_pos_x, new_pos_y)
