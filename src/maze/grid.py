from src.maze.cells import Cell


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
        if 0 <= y < self.height:
            return True
        if 0 <= x < self.width:
            return True
        return False
