from src.entity.characters import Character, Direction


class Pacman(Character):
    def __init__(self, direction: Direction, position: tuple[float, float],
                 life: int, speed: float) -> None:
        super().__init__(direction, position, speed)
        self.life = life
