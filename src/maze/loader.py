from mazegenerator import MazeGenerator
from src.entity.characters import Direction
from src.maze.grid import Grid
from src.maze.cell import Cell, CellContents
from src.message.errors import GridError

# Wall encoding of the mazegenerator package: one bit per side,
# set to 1 when there is a wall (N = 1, E = 2, S = 4, W = 8).
WALL_BITS = {Direction.UP: 1,
             Direction.DOWN: 4,
             Direction.RIGHT: 2,
             Direction.LEFT: 8}
# Cell closed on its 4 sides: part of the '42' pattern, unreachable.
CLOSED_CELL = 15


def convert_number_to_walls(number: int) -> set[Direction]:
    """Convert a cell number from the generator into a set of walls.

    Args:
        number (int): The cell as encoded by mazegenerator
            (see WALL_BITS).

    Returns:
        set[Direction]: The sides of the cell that have a wall.
    """
    walls: set[Direction] = set()
    for direction, bit in WALL_BITS.items():
        if (number & bit) != 0:
            walls.add(direction)
    return walls


def transform_maze_to_grid(maze: list[list[int]]) -> Grid:
    """Build a Grid from the maze returned by the generator.

    Every open cell gets a pacgum, the 4 corners get a super-pacgum,
    and the center (Pac-Man's start) and the closed cells stay empty.

    Args:
        maze (list[list[int]]): The generator's maze, indexed
            maze[y][x], each cell encoded as in WALL_BITS.

    Returns:
        Grid: The grid of cells ready for the game.
    """
    cells: list[list[Cell]] = []
    for number_row in maze:
        row: list[Cell] = []
        for number in number_row:
            walls = convert_number_to_walls(number)
            content = (CellContents.EMPTY if number == CLOSED_CELL
                       else CellContents.PACGUM)
            row.append(Cell(walls, content))
        cells.append(row)

    grid = Grid(cells)
    for y, x in grid.corners_grid():
        cell = grid.get_cell(y, x)
        cell.content = CellContents.SUPER_PACGUM
    y, x = grid.center_grid()
    center_cell = grid.get_cell(y, x)
    center_cell.content = CellContents.EMPTY

    return grid


def generate_maze(height: int, width: int, seed: int) -> Grid:
    """Generate a maze with the mazegenerator package and build its Grid.

    Args:
        height (int): The number of rows of the maze.
        width (int): The number of columns of the maze.
        seed (int): The seed of the maze.

    Returns:
        Grid: The grid of cells ready for the game.

    Raises:
        GridError: If the generator fails (e.g. invalid size).
    """
    try:
        generator = MazeGenerator(size=(width, height),
                                  perfect=False,
                                  seed=seed)
    except Exception as e:
        raise GridError("Maze generation failed "
                        f"(width={width}, height={height}, "
                        f"seed={seed}): {e}") from e

    maze = generator.maze
    grid = transform_maze_to_grid(maze)

    return grid
