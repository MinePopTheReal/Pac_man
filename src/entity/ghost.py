from src.entity.characters import Character, Direction
from enum import Enum, auto
from abc import abstractmethod
import math

SPEEDY_AHEAD = 4
BASHFUL_AHEAD = 2
POKEY_SHY_DISTANCE = 8


class GhostState(Enum):
    HUNTER = auto()
    HUNTED = auto()
    EATEN = auto()


class Ghost(Character):
    name: str = "ghost"

    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        super().__init__(direction, position, speed)
        self.state = state
        self.respawn_timer: float = 0.0

    @abstractmethod
    def position_target(self, pac_cell: tuple[int, int],
                        pac_direction: Direction,
                        shadow_cell: tuple[int, int],
                        corner: tuple[int, int]) -> tuple[int, int]:
        pass


class Shadow(Ghost):
    name: str = "blinky"

    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        super().__init__(direction, position, state, speed)

    def position_target(self, pac_cell: tuple[int, int],
                        pac_direction: Direction,
                        shadow_cell: tuple[int, int],
                        corner: tuple[int, int]) -> tuple[int, int]:
        return pac_cell


class Speedy(Ghost):
    name: str = "pinky"

    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        super().__init__(direction, position, state, speed)

    def position_target(self, pac_cell: tuple[int, int],
                        pac_direction: Direction,
                        shadow_cell: tuple[int, int],
                        corner: tuple[int, int]) -> tuple[int, int]:
        y, x = pac_cell
        dy, dx = pac_direction.value
        return (y + dy * SPEEDY_AHEAD, x + dx * SPEEDY_AHEAD)


class Bashful(Ghost):
    name: str = "inky"

    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        super().__init__(direction, position, state, speed)

    def position_target(self, pac_cell: tuple[int, int],
                        pac_direction: Direction,
                        shadow_cell: tuple[int, int],
                        corner: tuple[int, int]) -> tuple[int, int]:
        y, x = pac_cell
        dy, dx = pac_direction.value
        piv_y = y + dy * BASHFUL_AHEAD
        piv_x = x + dx * BASHFUL_AHEAD
        shad_y, shad_x = shadow_cell
        return (2 * piv_y - shad_y, 2 * piv_x - shad_x)


class Pokey(Ghost):
    name: str = "clyde"

    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        super().__init__(direction, position, state, speed)

    def position_target(self, pac_cell: tuple[int, int],
                        pac_direction: Direction,
                        shadow_cell: tuple[int, int],
                        corner: tuple[int, int]) -> tuple[int, int]:
        distance = math.dist(self.position, pac_cell)
        if distance > POKEY_SHY_DISTANCE:
            return pac_cell
        return corner
