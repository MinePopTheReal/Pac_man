import math
from src.maze.grid import Grid, LST_DIRECTION
from src.entity.characters import Direction


def direction_toward(grid: Grid, y: int, x: int, current: Direction,
                     dist_map: list[list[int]]) -> Direction:
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
            if distance < best_distance:
                best_direction = direction
                best_distance = distance

    if best_direction == Direction.NONE and grid.can_move(y, x, opposite):
        return opposite
    return best_direction
