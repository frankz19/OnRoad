import os
from typing import List, Any
import settings

USER_HOME = os.path.expanduser("~")
ONROAD_DIR = os.path.join(USER_HOME, ".onroad")
HIGHSCORES_PATH = os.path.join(ONROAD_DIR, "highscores.dat")


def read_highscores() -> List[List[Any]]:
    if not os.path.exists(ONROAD_DIR):
        os.mkdir(ONROAD_DIR)

    if not os.path.exists(HIGHSCORES_PATH):
        default_scores = [["AAA", 0] for _ in range(settings.NUM_HIGHSCORES)]
        save_high_scores(default_scores)

    highscores = []

    with open(HIGHSCORES_PATH, "r") as f:
        for line in f:
            data = line.strip().split(":")
            if len(data) == 2:
                highscores.append([data[0], int(data[1])])

    while len(highscores) < settings.NUM_HIGHSCORES:
        highscores.append(["AAA", 0])

    return highscores

def save_high_scores(highscores: List[List[Any]]) -> None:
    with open(HIGHSCORES_PATH, "w") as f:
        for score in highscores:
            f.write(f"{score[0]}:{score[1]}\n")

def add_high_score(highscores: List[List[Any]], name: str, score: int) -> None:

    highscores.append([name, score])
    highscores.sort(key=lambda x: x[1], reverse=True)

    if len(highscores) > settings.NUM_HIGHSCORES:
        highscores.pop()