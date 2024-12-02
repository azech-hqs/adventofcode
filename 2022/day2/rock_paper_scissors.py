from typing import Tuple
import sys


POINTS = {
    "X": 1, # A rock
    "Y": 2, # B paper
    "Z": 3, # C scissors
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

SHAPE_VALUE = {
    "A": 1,
    "B": 2,
    "C": 3,
}

RESPONSE = {
    "A": {
        "X": "C",
        "Y": "A",
        "Z": "B",
    },
    "B": {
        "X": "A",
        "Y": "B",
        "Z": "C",
    },
    "C": {
        "X": "B",
        "Y": "C",
        "Z": "A",
    },
}

def calculate_score(p1: str, p2: str) -> int:
    return OUTCOME[p1][p2] + POINTS[p2]

def calculate_score_2(p1: str, outcome: str) -> int:
    response = RESPONSE[p1][outcome]
    print(f"player1 played {p1}, your response is {response}")
    return ROUND_POINTS[outcome] + SHAPE_VALUE[response]

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        content = f.read()

    games = [line.split(" ") for line in content.rstrip("\n").split("\n")]
    game_points_1 = [calculate_score(*game) for game in games]
    game_points_2 = [calculate_score_2(*game) for game in games]

    print(f"There have been {len(game_points_1)} games.")
    print(f"You gained {sum(game_points_1)} points.")
    print(20*"-")
    print(f"Ultra top secret strategy:")
    print(f"Your total score is {sum(game_points_2)} points.")

