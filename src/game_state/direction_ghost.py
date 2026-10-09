import math
from src.maze.grid import Grid, LST_DIRECTION
from src.entity.characters import Direction


def direction_toward(grid: Grid, y: int, x: int, current: Direction,
                     target: tuple[int, int]) -> Direction:
    dir_y, dir_x = current.value
    opposite = Direction((-dir_y, -dir_x))
    best_direction: Direction = Direction.NONE
    best_distance: float = math.inf

    for direction in LST_DIRECTION:
        if direction == opposite:
            continue
        if grid.can_move(y, x, direction):
            dy, dx = direction.value
            neighbor = (y + dy, x + dx)
            distance = math.dist(neighbor, target)
            if distance < best_distance:
                best_direction = direction
                best_distance = distance

    if best_direction == Direction.NONE and grid.can_move(y, x, opposite):
        return opposite
    return best_direction
