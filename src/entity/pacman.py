from .characters import Character


class Pacman(Character):
    def __init__(self, direction: str, postion: tuple[int, int],
                 state: str, life: int) -> None:
        super().__init__(direction, postion, state)
        self.life = life
