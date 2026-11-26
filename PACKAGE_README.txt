PAC-MAN
=======

HOW TO RUN
----------
Run the "./pac-man <config_filename>" (by default config.json) executable located in this folder.

CONTROLS
--------
Menus:
  Up / Down arrows   Move the selection
  Enter              Select
  Esc                Go back to the previous menu / quit

In game:
  W A S D            Move Pac-Man
  Esc                Pause (see the note below)

CHEATS
------
Enable cheat mode with C

Available cheat:
|          Method          |                       Effect                       | key |
|--------------------------|----------------------------------------------------|-----|
|  `switch_cheat_mode()`   | turn the cheat mode on / off                       |  c  |
|  `switch_invincible()`   | ghosts cannot kill Pac-Man (he can still eat them) |  1  |
| `switch_ghosts_frozen()` | ghosts stop moving                                 |  2  |
|      `skip_level()`      | finish the level at once (wins after the last one) |  3  |
|    `add_extra_life()`    | one more life                                      |  4  |
| `switch_speed_pacman()`  | Pac-Man twice as fast                              |  5  |
|  `switch_slow_ghosts()`  | ghosts twice as slow                               |  6  |

CONFIGURATION
-------------
The config.json file, next to the executable, can be edited to change:
- <option>: <what it does>

HIGH SCORES
-----------
Your best scores are saved in the high_score/ folder, next to the executable.