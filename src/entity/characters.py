from .entity import Entity


class Character(Entity):
    def __init__(self, direction: str, postion: tuple[int, int],
                 state: str) -> None:
        super().__init__(postion, state)
        self.direction = direction
