from abc import ABC


class Entity(ABC):
    """Abstract class entity. """
    def __init__(self, position: tuple[float, float],
                 state: str) -> None:
        """initialization class entity.

        Args:
            position (tuple[float, float]): Cell: (y, x) row, column
            state (str): Entity's state.
        """
        self.position = position
        self.state = state
