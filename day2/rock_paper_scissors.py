from typing import Tuple
import sys


POINTS = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}


OUTCOME = {
    "A": {
        "X": 3,
        "Y": 6,
        "Z": 0,
    },
    "B": {
        "X": 0,
        "Y": 3,
        "Z": 6,
    },
    "C": {
        "X": 6,
        "Y": 0,
        "Z": 3,
    }
}

ROUND_POINTS = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}

# make a map of [A][Y] -> A

def calculate_score(shapes: Tuple[str, str]) -> int:
    p1, p2 = shapes
    return OUTCOME[p1][p2] + POINTS[p2]


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        content = f.read()

    games = [line.split(" ") for line in content.rstrip("\n").split("\n")]
    game_points_1 = [calculate_score(game) for game in games]
    game_points_2 = []

    print(f"There have been {len(game_points_1)} games.")
    print(f"You gained {sum(game_points_1)} points.")
