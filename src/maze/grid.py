from src.maze.pacgum_type import PacgumType
from src.entity.direction import Direction
from src.message.errors import GridError
from src.maze.cell import Cell


from collections import deque


LST_DIRECTION = [
    Direction.UP,
    Direction.DOWN,
    Direction.LEFT,
    Direction.RIGHT
]


class Grid:
    """The maze as a grid of cells.

    Cells are accessed as grid[y][x]: x is the row (0 at the top),
    y is the column (0 on the left).
    """

    def __init__(self, cells: list[list[Cell]]) -> None:
        """Create the cells and compute its size.

        Args:
            cells (list[list[Cell]]): The rows of the maze, each row
                being a list of cells. All rows must have the same length.
        """
        self.cells = cells
        self.height = len(self.cells)
        self.width = len(self.cells[0])

        self.pacgums: dict[tuple[int, int], PacgumType] = {}

    def in_grid(self, x: int, y: int) -> bool:
        """Check if a position is inside the grid.

        Args:
            x (int): The row.
            y (int): The column.

        Returns:
            bool: True if (x, y) is a cell of the grid, False otherwise.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def get_cell(self, x: int, y: int) -> Cell:
        """Return the cell at the given position.

        Args:
            x (int): The row.
            y (int): The column.

        Returns:
            Cell: The cell at (x, y).

        Raises:
            GridError: If (x, y) is outside the grid.
        """
        if not self.in_grid(x, y):
            raise GridError(
                f"coordinates ({x},{y}) are not in the grid, "
                f"grid size is {self.height} * {self.width}"
            )
        return self.cells[y][x]

    def has_wall(self, x: int, y: int, direction: Direction) -> bool:
        """Check if the cell at (x, y) has a wall on the given side.

        Args:
            x (int): The row.
            y (int): The column.
            direction (Direction): The side to check.

        Returns:
            bool: True if there is a wall on that side, False otherwise.
                Direction.NONE always returns False.

        Raises:
            GridError: If (x, y) is outside the grid.
        """
        cell = self.get_cell(x, y)
        return cell.there_is_wall(direction)

    def can_move(self, x: int, y: int, direction: Direction) -> bool:
        """Check if a character can go from (x, y) to the next cell.

        The move is allowed if there is no wall on that side of the cell
        and the next cell is inside the grid.

        Args:
            x (int): The row of the current cell.
            y (int): The column of the current cell.
            direction (Direction): The direction of the move.

        Returns:
            bool: True if the move is allowed, False otherwise.
                Direction.NONE always returns False, because it does not
                lead to another cell.

        Raises:
            GridError: If (x, y) is outside the grid.
        """
        if direction == Direction.NONE:
            return False

        if self.has_wall(x, y, direction):
            return False

        dx, dy = direction.value
        ny = y + dy
        nx = x + dx

        return self.in_grid(nx, ny)

    @property
    def center_grid(self) -> tuple[int, int]:
        """Return the position of the middle cell of the grid.

        Pac-Man starts on this cell and respawns on it after losing a life.
        If a size is even, there is no exact middle: the cell just before
        the middle is chosen (e.g. row 1 for a height of 4).

        Returns:
            tuple[int, int]: The (x, y) position of the middle cell.
        """
        center_y = (self.height - 1) // 2
        center_x = (self.width - 1) // 2
        return (center_x, center_y)

    @property
    def corners_grid(self) -> list[tuple[int, int]]:
        """Return the positions of the 4 corners of the grid.

        Used to place the ghosts and the super-pacgums. The order is
        always the same: top left, top right, bottom left, bottom right.

        Returns:
            list[tuple[int, int]]: The (x, y) positions of the 4 corners.
        """
        lst_corners: list[tuple[int, int]]
        top_left = (0, 0)
        top_right = (self.width - 1, 0)
        bot_left = (0, self.height - 1)
        bot_right = (self.width - 1, self.height - 1)
        lst_corners = [top_left, top_right, bot_left, bot_right]
        return lst_corners

    def remaining_pacgums(self) -> int:
        """Count the cells that still contain something to eat.

        Super-pacgums are counted: the level is won only when the maze
        is empty.

        Returns:
            int: The number of pacgums and super-pacgums left.
        """
        return len(self.pacgums)

    def distances_from_cell(self, x0: int, y0: int) -> list[list[int]]:
        dist = [[-1 for _ in range(self.width)] for _ in range(self.height)]
        dist[y0][x0] = 0
        queue: deque[tuple[int, int]] = deque([(x0, y0)])

        while queue:
            x, y = queue.popleft()
            for direction in LST_DIRECTION:
                if self.can_move(x, y, direction):
                    dx, dy = direction.value
                    ny = y + dy
                    nx = x + dx
                    if dist[ny][nx] == -1:
                        dist[ny][nx] = dist[y][x] + 1
                        queue.append((nx, ny))

        return dist
