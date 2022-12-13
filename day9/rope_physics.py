import sys
import numpy as np
from typing import List

def get_content(filename: str) -> List[List[str]]:
    with open(filename, "r") as f:
        content = f.read()
    content = content.rstrip("\n").split("\n")
    return [c.split(" ") for c in content]


MOVE = {
    "R": np.array([1, 0]),
    "L": np.array([-1,0]),
    "U": np.array([0, 1]),
    "D": np.array([0,-1]),
}


class Rope:
    def __init__(self, n_knots: int = 2) -> None:
        self.head = np.array([0,0])
        self.tail = np.array([0,0])
        self.n_knots = n_knots
        self.knots = np.zeros((n_knots, 2), dtype=int)
        self.visited = []

    def move(self, direction: str, steps: int) -> None:
        print(f"== {direction} {steps} ==")
        for i in range(0, steps):
            self.head += MOVE[direction]
            self.move_tail()
            self.add_to_visited(self.tail)
            self.print()

    def move_alt(self, direction: str, steps: int) -> None:
        print(f"== {direction} {steps} ==")
        for i in range(0, steps):
            self.knots[0] += MOVE[direction]
            for k in range(self.n_knots):
                self.move_knot(k)
            self.add_to_visited(self.knots[-1])
            # self.print_knots()

    def move_knot(self, index: int) -> None:
        if index == 0:
            return
        diff = self.knots[index-1] - self.knots[index]
        if np.all(np.abs(diff) <= 1):
            return
        comps = diff * np.identity(2)
        for i in range(2):
            if any(comps[i]):
                d = comps[i] / np.linalg.norm(comps[i])
                self.knots[index] += d.astype(int)
        

    def move_tail(self) -> None:
        diff = self.head - self.tail
        if np.all(np.abs(diff) <= 1):
            return
        comps = diff * np.identity(2)
        for i in range(2):
            if any(comps[i]):
                d = comps[i] / np.linalg.norm(comps[i])
                self.tail += d.astype(int)

    def add_to_visited(self, coordinate: np.ndarray) -> None:
        if not coordinate.tolist() in self.visited:
            self.visited.append(coordinate.tolist())

    def print(self):
        print(f"H: ({self.head[0]},{self.head[1]})")
        print(f"T: ({self.tail[0]},{self.tail[1]})")
        print("-"*10)

    def print_knots(self):
        print(self.knots)
        print("-"*10)

if __name__ == "__main__":
    movements = get_content(sys.argv[1])
    # part 1
    rope = Rope(n_knots=2)
    for movement in movements:
        rope.move(movement[0], int(movement[1]))
    print(f"Tail visited {len(rope.visited)} distinct coordinates")

    # part 2
    long_rope = Rope(n_knots=10)
    for movement in movements:
        long_rope.move_alt(movement[0], int(movement[1]))
    print(f"Tail visited {len(long_rope.visited)} distinct coordinates")

