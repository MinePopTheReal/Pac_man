from .entity import Entity


class Pacgum(Entity):
    def __init__(self, position: tuple[int, int], state: str) -> None:
        super().__init__(position, state)


class SuperPacgum(Pacgum):
    def __init__(self, position: tuple[int, int], state: str) -> None:
        # TODO: create class Case to represente a case of the maze
        super().__init__(position, state)
