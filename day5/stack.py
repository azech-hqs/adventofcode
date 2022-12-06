import sys
from typing import List
import re


STACK_WIDTH = 4

Stacks = List[List[str]]

def parse_stacks(content: str) -> Stacks:
    lines = content.split("\n")
    n_chars = len(lines[0])
    n_stacks, rem = divmod(n_chars+1, STACK_WIDTH)
    stacks = [[] for x in range(n_stacks)]
    for line in lines:
        if line[1] == "1":
            break
        for i in range(n_stacks):
            crate = line[1+STACK_WIDTH*i]
            if not str.isspace(crate):
                stacks[i].append(crate)
    return [stack[::-1] for stack in stacks]


def do_rearrangements(
        action_block: str,
        stacks: Stacks,
        multi_crate: bool = False) -> Stacks:
    print(f"Using CrateMover 900{int(multi_crate)}")
    actions = re.findall(r"move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)", action_block)

    for action in actions:
        n, i, k = list(map(int, action))
        # print(f"moving {n} item(s) from stack {i} to {k}")
        if n == 1:
            stacks[k-1].append(stacks[i-1].pop())
        elif multi_crate:
            stacks[k-1].extend(stacks[i-1][-n:])
            del stacks[i-1][-n:]
        else:
            stacks[k-1].extend(stacks[i-1][-1:-n-1:-1])
            del stacks[i-1][-1:-n-1:-1]
    return stacks

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        content = f.read()

    top, actions = content.split("\n\n")
    stacks = parse_stacks(top)
    print(f"before rearrangement: {stacks}")
    rearr_stacks = do_rearrangements(actions, stacks, multi_crate=True)
    tops = "".join([s[-1] for s in stacks if len(s) > 0])
    print(f"after rearrangement: {rearr_stacks}")
    print(f"the top crate of the stacks are: {tops}")


