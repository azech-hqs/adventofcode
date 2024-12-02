from typing import List
import sys

def parse_calories(calorie_blocks: str, delimiter: str = "\n") -> List[int]:
    processed = calorie_blocks.rstrip(delimiter).lstrip(delimiter)
    calories = [c.split(delimiter) for c in processed.split(delimiter*2)]
    calories = [sum(list(map(int, elf))) for elf in calories]
    return calories


def top_n_elves(elf_calories: List[int], n: int) -> List[int]:
    return sorted(elf_calories, reverse=True)[:n]

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        content = f.read()

    calories_by_elf = parse_calories(content)

    print(f"There are {len(calories_by_elf)} elves.")
    print(f"The elf with the most calories carries a total of {max(calories_by_elf)}")

    # part 2
    top_3 = top_n_elves(calories_by_elf, 3)
    print(top_3)
    print(f"The top three elves carry a total of {sum(top_3)}")
