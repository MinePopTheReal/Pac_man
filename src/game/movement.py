"""Movement rules shared by Pac-Man and the ghosts.

Characters move smoothly (float positions, in cells), but walls can only
be checked on whole cells. The rule used here: a character can only
change direction when it stands exactly on a cell, and it always stops
on every cell it crosses, so it can never skip a wall check. The only
exception is turning back (see try_turn_around), which never crosses
a wall.
"""
from src.entity.character import Direction, Character
from src.maze.grid import Grid, LST_DIRECTION


from math import floor, ceil


def is_on_cell(coord: tuple[float, float]) -> bool:
    """Check if a position is exactly on a cell (both values are whole).

    Args:
        coord (tuple[float, float]): A (x, y) position, in cells.

    Returns:
        bool: True for (5.0, 3.0), False for (5.0, 3.4).
    """
    x, y = coord
    return x.is_integer() and y.is_integer()


def choose_direction(
    x: int,
    y: int,
    wanted: Direction,
    current: Direction,
    grid: Grid
) -> Direction:
    """Choose where a character standing on a cell goes next.

    It tries, in this order: the wanted direction (key pressed or ghost
    choice), then the current direction (keep going straight), then it
    stops.

    Args:
        x (int): The column of the cell.
        y (int): The row of the cell.
        wanted (Direction): The direction the character would like to take.
        current (Direction): The direction it is moving in.
        grid (Grid): The maze.

    Returns:
        Direction: The direction to take, or Direction.NONE if both are
            blocked by walls.
    """
    if grid.can_move(x, y, wanted):
        return wanted
    if grid.can_move(x, y, current):
        return current
    return Direction.NONE


def next_cell(
    coord: tuple[float, float],
    direction: Direction
) -> tuple[float, float]:
    """Return the next cell on the way, in the given direction.

    On a cell, it is the neighbour cell. Between two cells, it is the
    cell the character is heading to. Examples, moving right:
    (5.0, 3.0) -> (5.0, 4.0) and (5.0, 3.4) -> (5.0, 4.0).

    Args:
        coord (tuple[float, float]): The current (x, y) position.
        direction (Direction): The direction of the move.

    Returns:
        tuple[float, float]: The (x, y) position of the next cell.
    """
    x, y = coord
    dx, dy = direction.value

    if is_on_cell(coord):
        return (float(x + dx), float(y + dy))

    nx = ceil(x) if dx > 0 else floor(x) if dx < 0 else x
    ny = ceil(y) if dy > 0 else floor(y) if dy < 0 else y

    return (float(nx), float(ny))


def try_turn_around(pacman: Character, wanted: Direction) -> None:
    """Let Pac-Man turn back at once, even between two cells.

    Without it, he would only turn back on the next cell, which feels
    slow. No wall check is needed: he goes back to the cell he just
    left, so the way is free. On a cell, nothing is done here, because
    advance() already chooses the direction with the walls. Only used
    for Pac-Man: ghosts must not turn back whenever they want.

    Args:
        pacman (Character): The character to turn back; its direction
            is updated.
        wanted (Direction): The direction the player wants. Only the
            opposite of the current direction makes him turn back.
    """
    if is_on_cell(pacman.position):
        return

    dy, dx = pacman.direction.value
    opposite = Direction((-dy, -dx))

    if wanted == opposite:
        pacman.direction = wanted


def advance(
    character: Character,
    wanted: Direction,
    dt: float,
    grid: Grid
) -> None:
    """Move a character for one frame, without going through walls.

    1. If it stands on a cell, it chooses its direction (and stops if
       it is blocked).
    2. It moves towards the next cell by speed * dt.
    3. If it would reach or pass that cell, it is placed exactly on it,
       so the next frame can choose a direction again.

    The wanted direction is only used when the character is on a cell.

    Args:
        character (Character): Pac-Man or a ghost; its position and
            direction are updated.
        wanted (Direction): The direction it would like to take.
        dt (float): The time since the last frame, in seconds.
        grid (Grid): The maze.
    """
    if is_on_cell(character.position):
        px, py = character.position
        character.direction = choose_direction(
            int(px), int(py), wanted, character.direction, grid
        )
        if character.direction == Direction.NONE:
            return

    tx, ty = next_cell(character.position, character.direction)
    x, y = character.position
    remains = abs(tx - x) + abs(ty - y)

    distance = character.speed * dt
    if distance >= remains:
        character.position = (tx, ty)
    else:
        character.move(dt)


def direction_home(
    x: int, y: int, maze: list[list[int]], grid: Grid
) -> Direction:
    """Give the direction that brings an eaten ghost closer to its corner.

    It looks for the neighbour cell that is one step closer to the
    corner in the distance map.

    Args:
        y (int): The row of the ghost's cell.
        x (int): The column of the ghost's cell.
        maze (list[list[int]]): The distance map of the ghost's corner
            (see Grid.distances_from_cell).
        grid (Grid): The maze.

    Returns:
        Direction: The direction to take, or Direction.NONE if the ghost
            is already in its corner.
    """
    step = maze[y][x]
    if step <= 0:
        return Direction.NONE
    for direction in LST_DIRECTION:
        if grid.can_move(x, y, direction):
            dx, dy = direction.value
            ny = y + dy
            nx = x + dx
            if maze[ny][nx] == step - 1:
                return direction
    return Direction.NONE
