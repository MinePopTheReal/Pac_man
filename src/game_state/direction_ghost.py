import math
from src.maze.grid import Grid, LST_DIRECTION
from src.entity.characters import Direction


def direction_toward(grid: Grid, y: int, x: int, current: Direction,
                     dist_map: list[list[int]], run_away: bool) -> Direction:
    """Choose the direction that gets a ghost closer to its target.

    The ghost looks at its open neighbour cells and picks the one with
    the smallest distance in dist_map (or the largest when running
    away). It never turns back, unless it has no other way out.

    Args:
        grid (Grid): The maze.
        y (int): The row of the ghost's cell.
        x (int): The column of the ghost's cell.
        current (Direction): The direction the ghost is moving in.
        dist_map (list[list[int]]): Distance of every cell to the
            target (see Grid.distances_from_cell).
        run_away (bool): True to go away from the target instead.

    Returns:
        Direction: The direction to take, or Direction.NONE if blocked.
    """
    dir_y, dir_x = current.value
    opposite = Direction((-dir_y, -dir_x))
    best_direction: Direction = Direction.NONE
    best_distance: float = math.inf

    for direction in LST_DIRECTION:
        if direction == opposite:
            continue
        if grid.can_move(y, x, direction):
            dy, dx = direction.value
            ny = y + dy
            nx = x + dx
            distance = dist_map[ny][nx]
            if distance == -1:
                continue
            if run_away:
                distance = - distance
            if distance < best_distance:
                best_direction = direction
                best_distance = distance

    if best_direction == Direction.NONE and grid.can_move(y, x, opposite):
        return opposite
    return best_direction
