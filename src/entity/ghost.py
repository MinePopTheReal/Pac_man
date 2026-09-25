from .characters import Character, Direction
from enum import Enum, auto


class GhostState(Enum):
    HUNTER = auto()
    HUNTED = auto()
    EATEN = auto()


class Ghost(Character):
    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        super().__init__(direction, position, speed)
        self.state = state


class Shadow(Ghost):
    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        super().__init__(direction, position, state, speed)


class Speedy(Ghost):
    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        super().__init__(direction, position, state, speed)


class Bashful(Ghost):
    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        super().__init__(direction, position, state, speed)


class Pokey(Ghost):
    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        super().__init__(direction, position, state, speed)
