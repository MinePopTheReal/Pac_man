from enum import Enum


class PacgumState(Enum):
    pass


class Pacgum():
    def __init__(self, position: tuple[int, int], state: PacgumState) -> None:
        self.position = position
        self.state = state


class SuperPacgum(Pacgum):
    def __init__(self, position: tuple[int, int], state: PacgumState) -> None:
        # TODO: create class Case to represente a case of the maze
        super().__init__(position, state)
