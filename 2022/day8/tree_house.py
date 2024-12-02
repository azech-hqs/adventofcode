import sys
import numpy as np

def gen_patch_matrix(patch: str) -> np.ndarray:
    l = [list(map(int,list(row))) for row in patch.rstrip("\n").split("\n")]
    return np.array(l)

def check_visible(vec: np.ndarray, index: int) -> int:
    left, middle, right = np.split(vec, [index, index+1])
    if np.all(left < middle) or np.all(right < middle):
        return 1
    return 0


def get_visible(matrix: np.ndarray) -> int:
    rows, cols = matrix.shape
    always_vis = cols*2 + (rows - 2)*2

    inside_vis = 0
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            vis = check_visible(matrix[i], j)
            if vis == 0:
                vis = check_visible(matrix[:,j], i)
            inside_vis += vis
    print(f"always visible: {always_vis}")
    print(f"inside visible: {inside_vis}")
    return always_vis + inside_vis


def scenic_score(vec: np.ndarray, index: int) -> int:
    left, middle, right = np.split(vec, [index, index+1])
    # east = np.argwhere(right >= middle)
    east, west = 0, 0
    for i in range(len(right)):
        east += 1
        if right[i] >= middle[0]:
            break
    for i in range(-1, -1-len(left), -1):
        west += 1
        if left[i] >= middle[0]:
            break
    return east * west


def get_scenic_score(matrix: np.ndarray) -> int:
    rows, cols = matrix.shape
    max_score = 1
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            score_1 = scenic_score(matrix[i], j)
            print(f"row {i} - {j}: {score_1}")
            score_2 = scenic_score(matrix[:,j], i)
            print(f"col {j} - {i}: {score_2}")
            score = score_1 * score_2
            if score > max_score:
                max_score = score
    return max_score

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        content = f.read()

    patch_matrix = gen_patch_matrix(content)
    print(patch_matrix)

    visible = get_visible(patch_matrix)
    print("total visible:", visible)

    max_scenic_score = get_scenic_score(patch_matrix)
    print(f"highest scenic score = {max_scenic_score}")
