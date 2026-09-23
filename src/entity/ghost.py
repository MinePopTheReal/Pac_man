from .characters import Character


class Ghost(Character):
    def __init__(self, direction: str, postion: tuple[int, int], state: str,
                 speed: float) -> None:
        super().__init__(direction, postion, state)
        self.speed = speed


class Shadow(Ghost):
    def __init__(self, direction: str, postion: tuple[int, int], state: str,
                 speed: float) -> None:
        super().__init__(direction, postion, state, speed)


class Speedy(Ghost):
    def __init__(self, direction: str, postion: tuple[int, int], state: str,
                 speed: float) -> None:
        super().__init__(direction, postion, state, speed)


class Bashful(Ghost):
    def __init__(self, direction: str, postion: tuple[int, int], state: str,
                 speed: float) -> None:
        super().__init__(direction, postion, state, speed)


class Pokey(Ghost):
    def __init__(self, direction: str, postion: tuple[int, int], state: str,
                 speed: float) -> None:
        super().__init__(direction, postion, state, speed)
