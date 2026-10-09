from mazegenerator import MazeGenerator
from src.entity.characters import Direction
from src.maze.grid import Grid
from src.maze.cell import Cell, CellContents
from src.message.errors import GridError
from src.message.warning import WarningMessage
import random

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


def transform_maze_to_grid(maze: list[list[int]], nb_pacgums: int,
                           seed: int) -> Grid:
    """Build a Grid from the maze returned by the generator.

    The 4 corners get a super-pacgum. The pacgums are then placed at
    random on the free cells: every cell except the corners, the center
    (Pac-Man's start) and the closed cells of the '42' pattern.
    If there are not enough free cells, a warning is printed and every
    free cell gets a pacgum.

    Args:
        maze (list[list[int]]): The generator's maze, indexed
            maze[y][x], each cell encoded as in WALL_BITS.
        nb_pacgums (int): The number of pacgums to place, super-pacgums
            not included.
        seed (int): The seed used to choose the cells of the pacgums.

    Returns:
        Grid: The grid of cells ready for the game.
    """
    cells: list[list[Cell]] = []
    free_cell: list[tuple[int, int]] = []
    for y, number_row in enumerate(maze):
        row: list[Cell] = []
        for x, number in enumerate(number_row):
            walls = convert_number_to_walls(number)
            content = CellContents.EMPTY
            row.append(Cell(walls, content))
            if number != CLOSED_CELL:
                free_cell.append((y, x))
        cells.append(row)

    grid = Grid(cells)
    for y, x in grid.corners_grid:
        cell = grid.get_cell(y, x)
        cell.content = CellContents.SUPER_PACGUM
        free_cell.remove((y, x))
    y, x = grid.center_grid
    free_cell.remove((y, x))

    if nb_pacgums > len(free_cell):
        print(WarningMessage(f"The number of pacgums ({nb_pacgums}) exceeds "
                             f"the number of free cells ({len(free_cell)}), "
                             f"using {len(free_cell)} instead."))
        nb_pacgums = len(free_cell)

    rng = random.Random(seed) if seed != 0 else random.Random()
    lst_cell_pac = rng.sample(free_cell, nb_pacgums)

    for y, x in lst_cell_pac:
        cell = grid.get_cell(y, x)
        cell.content = CellContents.PACGUM

    return grid


def generate_maze(height: int, width: int, seed: int, nb_pacgums: int) -> Grid:
    """Generate a maze with the mazegenerator package and build its Grid.

    Args:
        height (int): The number of rows of the maze.
        width (int): The number of columns of the maze.
        seed (int): The seed of the maze. 0 gives a random maze.
        nb_pacgums (int): The number of pacgums to place, super-pacgums
            not included.

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
    grid = transform_maze_to_grid(maze, nb_pacgums, seed)

    return grid
