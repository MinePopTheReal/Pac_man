import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
print(ROOT)

def bundle_dir() -> Path:
    """Fichiers embarqués en lecture seule (assets)."""
    return Path(getattr(sys, "_MEIPASS", ROOT))


def app_dir() -> Path:
    """Fichiers modifiables : config.json, high_score/."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return ROOT