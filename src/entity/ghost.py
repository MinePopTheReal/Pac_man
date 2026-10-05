from src.entity.characters import Character, Direction
from enum import Enum, auto


class GhostState(Enum):
    HUNTER = auto()
    HUNTED = auto()
    EATEN = auto()


class Ghost(Character):
    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float,
                 respawn_timer: float = 0.0) -> None:
        super().__init__(direction, position, speed)
        self.state = state
        self.respawn_timer = respawn_timer


class Shadow(Ghost):
    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float,
                 respawn_timer: float) -> None:
        super().__init__(direction, position, state, speed, respawn_timer)


class Speedy(Ghost):
    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float,
                 respawn_timer: float) -> None:
        super().__init__(direction, position, state, speed, respawn_timer)


class Bashful(Ghost):
    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float,
                 respawn_timer: float) -> None:
        super().__init__(direction, position, state, speed, respawn_timer)


class Pokey(Ghost):
    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float,
                 respawn_timer: float) -> None:
        super().__init__(direction, position, state, speed, respawn_timer)
