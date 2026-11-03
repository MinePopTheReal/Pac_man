def format_time(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    return f"{"time":>5}: {minutes}:{secs:02d}"

def format_lives(lives: int) -> str:
    return f"{"lives":>5}: " + "❤" * min(lives, 3) + ("+" if lives > 3 else "")

def format_level(level: int) -> str:
    return f"{"level":>5}: " + str(level)

def format_score(score: int) -> str:
    return f"{"score":>5}: " + str(score)