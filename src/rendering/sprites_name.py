from src.maze.grid import Direction


_SUFFIX_BY_DIRECTION = {
    Direction.UP: "top",
    Direction.RIGHT: "right",
    Direction.DOWN: "bottom",
    Direction.LEFT: "left"
}

# pacman
PACMAN_BY_DIRECTION = {d: f"pacman_{s}" for d, s in _SUFFIX_BY_DIRECTION.items()}
PACMAN_DEATH = "pacman_death"

# ghosts
_GHOSTS_NAMES = (
    "clyde",
    "inky",
    "pinky",
    "blinky"
)

GHOSTS_BY_DIRECTION = {ghost_name: {d: f"{ghost_name}_{s}" for d, s in _SUFFIX_BY_DIRECTION.items()}for ghost_name in _GHOSTS_NAMES}
EYES_BY_DIRECTION = {d: f"ghosts_eyes_{s}" for d, s in _SUFFIX_BY_DIRECTION.items()}
GHOST_FEAR_BLUE = "ghosts_fear_blue"
GHOST_FEAR_WHITE = "ghosts_fear_white"

# pacgum
PACGUM = "pacgum"
SUPER_PACGUM = "super_pacgum"
