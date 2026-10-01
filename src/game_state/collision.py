import math

COLLIDES_DISTANCE = 0.5


def collides(character_a: tuple[float, float],
             character_b: tuple[float, float]) -> bool:
    return math.dist(character_a, character_b) < COLLIDES_DISTANCE
