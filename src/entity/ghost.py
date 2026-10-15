from src.entity.characters import Character, Direction
from enum import Enum, auto
from abc import abstractmethod
import math

# How many cells in front of Pac-Man Speedy aims at.
SPEEDY_AHEAD = 4
# How many cells in front of Pac-Man Bashful's pivot is.
BASHFUL_AHEAD = 2
# Pokey goes back to his corner when he is closer than this to Pac-Man.
POKEY_SHY_DISTANCE = 8


class GhostState(Enum):
    """What a ghost is doing.

    HUNTER: chases Pac-Man (touching him costs a life).
    HUNTED: runs away, can be eaten (after a super-pacgum).
    EATEN: going back to its corner, then waits before hunting again.
    """
    HUNTER = auto()
    HUNTED = auto()
    EATEN = auto()


class Ghost(Character):
    """A ghost: a character with a state and its own way of chasing.

    Each kind of ghost (Shadow, Speedy, Bashful, Pokey) chooses a
    different target cell, see position_target.

    Attributes:
        name (str): Sprite name of the ghost ("blinky", "pinky", ...).
        state (GhostState): What the ghost is doing.
        respawn_timer (float): Seconds left before an eaten ghost hunts
            again, once it is back in its corner.
    """
    name: str = "ghost"

    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        """Create a ghost.

        Args:
            direction (Direction): Starting direction.
            position (tuple[float, float]): Starting (y, x) position, in cells.
            state (GhostState): Starting state.
            speed (float): Speed in cells per second.
        """
        super().__init__(direction, position, speed)
        self.state = state
        self.respawn_timer: float = 0.0

    @abstractmethod
    def position_target(self, pac_cell: tuple[int, int],
                        pac_direction: Direction,
                        shadow_cell: tuple[int, int],
                        corner: tuple[int, int]) -> tuple[int, int]:
        """Give the cell this ghost aims at while it is hunting.

        The cell may be a wall or outside the maze: GameState checks it.

        Args:
            pac_cell (tuple[int, int]): Pac-Man's (y, x) cell.
            pac_direction (Direction): The direction Pac-Man is moving in.
            shadow_cell (tuple[int, int]): Shadow's (y, x) cell.
            corner (tuple[int, int]): This ghost's own corner.

        Returns:
            tuple[int, int]: The (y, x) cell to aim at.
        """
        pass


class Shadow(Ghost):
    """Blinky: follows Pac-Man closely."""
    name: str = "blinky"

    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        """Create the ghost (see Ghost.__init__)."""

        super().__init__(direction, position, state, speed)

    def position_target(self, pac_cell: tuple[int, int],
                        pac_direction: Direction,
                        shadow_cell: tuple[int, int],
                        corner: tuple[int, int]) -> tuple[int, int]:
        """Aim straight at Pac-Man's cell."""
        return pac_cell


class Speedy(Ghost):
    """Pinky: tries to cut Pac-Man off."""
    name: str = "pinky"

    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        """Create the ghost (see Ghost.__init__)."""

        super().__init__(direction, position, state, speed)

    def position_target(self, pac_cell: tuple[int, int],
                        pac_direction: Direction,
                        shadow_cell: tuple[int, int],
                        corner: tuple[int, int]) -> tuple[int, int]:
        """Aim SPEEDY_AHEAD cells in front of Pac-Man."""
        y, x = pac_cell
        dy, dx = pac_direction.value
        return (y + dy * SPEEDY_AHEAD, x + dx * SPEEDY_AHEAD)


class Bashful(Ghost):
    """Inky: traps Pac-Man together with Shadow."""
    name: str = "inky"

    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        """Create the ghost (see Ghost.__init__)."""

        super().__init__(direction, position, state, speed)

    def position_target(self, pac_cell: tuple[int, int],
                        pac_direction: Direction,
                        shadow_cell: tuple[int, int],
                        corner: tuple[int, int]) -> tuple[int, int]:
        """Aim at the side of Pac-Man opposite to Shadow.

        The target is Shadow's position mirrored through the cell
        BASHFUL_AHEAD cells in front of Pac-Man.
        """
        y, x = pac_cell
        dy, dx = pac_direction.value
        piv_y = y + dy * BASHFUL_AHEAD
        piv_x = x + dx * BASHFUL_AHEAD
        shad_y, shad_x = shadow_cell
        return (2 * piv_y - shad_y, 2 * piv_x - shad_x)


class Pokey(Ghost):
    """Clyde: chases Pac-Man, but runs home when too close."""
    name: str = "clyde"

    def __init__(self, direction: Direction, position: tuple[float, float],
                 state: GhostState, speed: float) -> None:
        """Create the ghost (see Ghost.__init__)."""

        super().__init__(direction, position, state, speed)

    def position_target(self, pac_cell: tuple[int, int],
                        pac_direction: Direction,
                        shadow_cell: tuple[int, int],
                        corner: tuple[int, int]) -> tuple[int, int]:
        """Aim at Pac-Man when far from him, else at the own corner.

        "Far" means more than POKEY_SHY_DISTANCE cells, in straight line.
        """
        distance = math.dist(self.position, pac_cell)
        if distance > POKEY_SHY_DISTANCE:
            return pac_cell
        return corner
