import math
from src.entity.characters import Direction, Character
from src.maze.grid import Grid, LST_DIRECTION


def is_on_cell(coord: tuple[float, float]) -> bool:
    y, x = coord
    return y.is_integer() and x.is_integer()


def choose_direction(y: int, x: int, wanted: Direction, current: Direction,
                     grid: Grid) -> Direction:
    if grid.can_move(y, x, wanted):
        return wanted
    if grid.can_move(y, x, current):
        return current
    return Direction.NONE


def next_cell(coord: tuple[float, float],
              direction: Direction) -> tuple[float, float]:
    y, x = coord
    dy, dx = direction.value

    if is_on_cell(coord):
        return (float(y + dy), float(x + dx))

    ny = math.ceil(y) if dy > 0 else math.floor(y) if dy < 0 else y
    nx = math.ceil(x) if dx > 0 else math.floor(x) if dx < 0 else x

    return (float(ny), float(nx))


def advance(character: Character, wanted: Direction, dt: float,
            grid: Grid) -> None:
    if is_on_cell(character.position):
        py, px = character.position
        character.direction = choose_direction(
            int(py), int(px), wanted, character.direction, grid)
        if character.direction == Direction.NONE:
            return

    ty, tx = next_cell(character.position, character.direction)
    y, x = character.position
    remains = abs(ty - y) + abs(tx - x)

    distance = character.speed * dt
    if distance >= remains:
        character.position = (ty, tx)
    else:
        character.move(dt)


def direction_home(y: int, x: int, mapp: list[list[int]],
                   grid: Grid) -> Direction:
    d = mapp[y][x]
    if d <= 0:
        return Direction.NONE
    for direction in LST_DIRECTION:
        if grid.can_move(y, x, direction):
            dy, dx = direction.value
            ny = y + dy
            nx = x + dx
            if mapp[ny][nx] == d - 1:
                return direction
    return Direction.NONE
