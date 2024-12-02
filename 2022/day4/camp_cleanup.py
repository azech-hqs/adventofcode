import sys
import re
from typing import Tuple, List

REGEX = r"(\d+)-(\d+)"


def get_pairs(line: str) -> List[Tuple[int,int]]:
    match = re.findall(REGEX, line)
    return [tuple(map(int, x)) for x in match]


def is_contained(limits: List[Tuple[int,int]]) -> int:
    elf1, elf2 = limits
    # section(elf1) within section(elf2)
    AinB = elf1[0] >= elf2[0] and elf1[1] <= elf2[1]
    # section(elf2) within section(elf1)
    BinA = elf1[0] <= elf2[0] and elf1[1] >= elf2[1]
    if AinB or BinA:
        return 1
    return 0

def overlaps(limits: List[Tuple[int,int]]) -> int:
    elf1, elf2 = limits

    # forward overlapping
    ov1 = elf1[0] < elf2[0] and elf1[1] < elf2[1] and elf1[1] >= elf2[0]
    # backward overlapping
    ov2 = elf1[0] > elf2[0] and elf1[1] > elf2[1] and elf1[0] <= elf2[1]
    if ov1 or ov2:
        return 1
    return 0

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        content = f.read()

    lines = content.rstrip("\n").split("\n")
    pairs = [get_pairs(line) for line in lines]

    within = [is_contained(x) for x in pairs]
    pairs_within = sum(within)

    print(f"There are {len(pairs)} pairs")
    print(f"of which {pairs_within} are contained within each other")

    # part2
    ov = [overlaps(x) for x in pairs]
    pairs_ov = pairs_within + sum(ov)
    print(f"and {pairs_ov} pairs in total overlap")
