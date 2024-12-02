import sys
from typing import Tuple, List

PRIORITIES = { chr(97+i):i+1 for i in range(26) }
PRIORITIES.update({ chr(65+i):i+27 for i in range(26) })

def split_compartments(rucksack: str) -> Tuple[str, str]:
    half = int(len(rucksack) / 2)
    return rucksack[:half], rucksack[half:]


def get_priority(rucksack: str) -> int:
    comp1, comp2 = [set(c) for c in split_compartments(rucksack)]
    common = comp1 & comp2
    if len(common) > 1:
        raise IndexError("Too many common items!")
    return [PRIORITIES[letter] for letter in common][0]

def get_group_priority(group: List[str]) -> int:
    sets = [set(r) for r in group]
    common = sets[0] & sets[1] & sets[2]
    if len(common) > 1:
        raise IndexError("Too many common items!")
    return [PRIORITIES[letter] for letter in common][0]

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        content = f.read()

    rucksacks = content.rstrip("\n").split("\n")
    nr = len(rucksacks)
    
    priorities = [get_priority(r) for r in rucksacks]

    print(f"There are {nr} rucksacks.")
    print(f"The combined priority of common items is {sum(priorities)}.")
    
    # part 2
    badge_prio = [get_group_priority(rucksacks[i:(i+3)]) for i in range(0, nr, 3)]
    print(20*"-")
    print(badge_prio)
    print(f"There are {len(badge_prio)} groups of elves.")
    print(f"The combined badge priority is {sum(badge_prio)}")
    
