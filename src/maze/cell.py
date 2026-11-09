from src.entity.characters import Direction


class Cell:
    """One cell of the maze: its walls and its content.

    The cell does not store its own coordinates: its position is given
    by its place in the maze grid (cells[y][x]).
    """

    def __init__(self, walls: set[Direction]) -> None:
        """Create a cell.

        Args:
            walls (set[Direction]): The sides of the cell that have a wall.
        """
        self.walls = walls

    def there_is_wall(self, direction: Direction) -> bool:
        """Check if the cell has a wall on the given side.

        Args:
            direction (Direction): The side to check.

        Returns:
            bool: True if there is a wall on that side, False otherwise.
                Direction.NONE always returns False.
        """
        for wall in self.walls:
            if wall == direction:
                return True
        return False
