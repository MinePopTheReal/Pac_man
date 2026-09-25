from src.maze.cells import Cell
from src.message.errors import GridError
from src.entity.characters import Direction


class Grid:
    """The maze as a grid of cells.

    Cells are accessed as grid[y][x]: y is the row (0 at the top),
    x is the column (0 on the left).
    """
    def __init__(self, grid: list[list[Cell]]) -> None:
        """Create the grid and compute its size.

        Args:
            grid (list[list[Cell]]): The rows of the maze, each row
                being a list of cells. All rows must have the same length.
        """
        self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def in_grid(self, y: int, x: int) -> bool:
        """Check if a position is inside the grid.

        Args:
            y (int): The row.
            x (int): The column.

        Returns:
            bool: True if (y, x) is a cell of the grid, False otherwise.
        """
        if 0 <= y < self.height and 0 <= x < self.width:
            return True
        return False

    def get_cell(self, y: int, x: int) -> Cell:
        """Return the cell at the given position.

        Args:
            y (int): The row.
            x (int): The column.

        Returns:
            Cell: The cell at (y, x).

        Raises:
            GridError: If (y, x) is outside the grid.
        """
        if not self.in_grid(y, x):
            raise GridError(f"coordinates ({y},{x}) are not in the grid, "
                            f"grid size is {self.height} * {self.width}")
        return self.grid[y][x]

    def has_wall(self, y: int, x: int, direction: Direction) -> bool:
        """Check if the cell at (y, x) has a wall on the given side.

        Args:
            y (int): The row.
            x (int): The column.
            direction (Direction): The side to check.

        Returns:
            bool: True if there is a wall on that side, False otherwise.
                Direction.NONE always returns False.

        Raises:
            GridError: If (y, x) is outside the grid.
        """
        cell = self.get_cell(y, x)
        return cell.there_is_wall(direction)

    def can_move(self, y: int, x: int, direction: Direction) -> bool:
        """Check if a character can go from (y, x) to the next cell.

        The move is allowed if there is no wall on that side of the cell
        and the next cell is inside the grid.

        Args:
            y (int): The row of the current cell.
            x (int): The column of the current cell.
            direction (Direction): The direction of the move.

        Returns:
            bool: True if the move is allowed, False otherwise.
                Direction.NONE always returns False, because it does not
                lead to another cell.

        Raises:
            GridError: If (y, x) is outside the grid.
        """
        if direction == Direction.NONE:
            return False

        if self.has_wall(y, x, direction):
            return False

        dy, dx = direction.value
        ny = y + dy
        nx = x + dx

        return self.in_grid(ny, nx)

    def center_grid(self) -> tuple[int, int]:
        """Return the position of the middle cell of the grid.

        Pac-Man starts on this cell and respawns on it after losing a life.
        If a size is even, there is no exact middle: the cell just before
        the middle is chosen (e.g. row 1 for a height of 4).

        Returns:
            tuple[int, int]: The (y, x) position of the middle cell.
        """
        center_y = (self.height - 1) // 2
        center_x = (self.width - 1) // 2
        return (center_y, center_x)

    def corners(self) -> list[tuple[int, int]]:
        return [(0, 0)]

    def remaining_pacgums(self) -> int:
        return 0
