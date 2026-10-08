import math

# Two characters touch when they are closer than this, in cells.
COLLIDES_DISTANCE = 0.5


def collides(character_a: tuple[float, float],
             character_b: tuple[float, float]) -> bool:
    """Check if two characters touch each other.

    The function only compares two positions: it does not know who the
    characters are. Deciding what happens (losing a life, eating a
    ghost) is done by GameState.

    Args:
        character_a (tuple[float, float]): The (y, x) position of the
            first character, in cells.
        character_b (tuple[float, float]): The (y, x) position of the
            second character, in cells.

    Returns:
        bool: True if they are closer than COLLIDES_DISTANCE.
    """
    return math.dist(character_a, character_b) < COLLIDES_DISTANCE
