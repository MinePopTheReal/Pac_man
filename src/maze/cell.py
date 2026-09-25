from enum import Enum, auto
from src.entity.characters import Direction


class CellContents(Enum):
    """What a cell of the maze can contain."""
    EMPTY = auto()
    PACGUM = auto()
    SUPER_PACGUM = auto()


class Cell:
    """One cell of the maze: its walls and its content.

    The cell does not store its own coordinates: its position is given
    by its place in the maze grid (cells[y][x]).
    """
    def __init__(self, walls: set[Direction], content: CellContents) -> None:
        """Create a cell.

        Args:
            walls (set[Direction]): The sides of the cell that have a wall.
            content (CellContents): What the cell contains.
        """
        self.walls = walls
        self.content = content

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

    def update_cell_content(self) -> CellContents:
        """Empty the cell and return what it contained before.

        Returns:
            CellContents: The content of the cell before it was emptied.
                EMPTY if the cell was already empty.
        """
        current_content = self.content
        self.content = CellContents.EMPTY
        return current_content
