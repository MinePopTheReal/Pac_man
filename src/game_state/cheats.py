from dataclasses import dataclass


@dataclass
class Cheats:
    """Which cheats are on, to help testing the game.

    GameState changes these values through its switch_... methods;
    the screens can read them to show which cheats are active.

    Attributes:
        enabled (bool): Cheat mode is on. The other cheats can only be
            switched while it is on.
        invincible (bool): Ghosts cannot kill Pac-Man.
        ghosts_frozen (bool): Ghosts do not move.
        fast (bool): Pac-Man moves twice as fast.
        slow (bool): Ghosts move twice as slow.
    """
    enabled: bool = False
    invincible: bool = False
    ghosts_frozen: bool = False
    fast: bool = False
    slow: bool = False
