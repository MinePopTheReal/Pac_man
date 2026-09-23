from abc import ABC


class Entity(ABC):
    def __init__(self, postion: tuple[int, int], state: str) -> None:
        self.position = postion
        self.state = state
