import sys
import re
from typing import Callable

def get_instructions(filename: str) -> list:
    with open(filename, "r") as f:
        content = f.read().rstrip("\n")
    pattern = r"^(\w+)\s*([-]?\d+)?"
    instructions = re.findall(pattern, content, re.MULTILINE)
    names, values = zip(*instructions)
    values = list(map(lambda x: int(x) if not x == "" else None, values))
    return list(zip(names, values))


CYCLES = {
    "addx": 2,
    "noop": 1,
}

class Instruction:
    def __init__(self, name: str = "noop", value: int = 0) -> None:
        self.n_cycles = CYCLES[name]
        self.name = name
        self.value = value
        self.counter = 0

    def execute(self, register_value: int) -> int:
        match self.name:
            case "addx":
                return register_value + self.value
            case _:
                return register_value

    def increment(self, incr: int = 1) -> None:
        self.counter += incr

    @property
    def is_finished(self):
        return self.n_cycles == self.counter

class CPU:
    def __init__(self, program: list) -> None:
        self.X = 1
        self.program = program
        self.iid = 0
        self.load_instruction()

    def run(self) -> None:
        self.current.increment()
        if self.current.is_finished:
            self.X = self.current.execute(self.X)
            self.iid += 1
            self.load_instruction()

    def load_instruction(self) -> None:
        if self.iid < len(self.program):
            self.current = Instruction(*self.program[self.iid])
        else:
            self.current = Instruction()

    def signal_strength(self, iteration) -> int:
        # print(f"{self.current.name} - {self.current.counter}")
        # print(f"signal({iteration}) = {self.X} * {iteration}")
        return iteration * self.X;

class CathodeRayTube:
    def __init__(self, sprite_width: int = 3) -> None:
        self.sprite_width = sprite_width
        self.position = 0

    def draw(self, sprite_position: int, screen_width: int = 40) -> str:
        diff = sprite_position - divmod(self.position, screen_width)[1]
        self.increment()
        if abs(diff) == 1 or abs(diff) == 0:
            return "#"
        return "."

    def increment(self) -> None:
        self.position += 1


if __name__ == "__main__":
    program = get_instructions(sys.argv[1])
    print(f"# of instructions: {len(program)}")
    signal_strengths = []
    max_cycles = 240
    cycle = 1
    cpu = CPU(program)
    crt = CathodeRayTube()
    pixels = []
    while cycle <= max_cycles:
        c = [20+(40*x) for x in range(6)]
        if cycle in c:
            signal_strengths.append(cpu.signal_strength(cycle))
        pixel = crt.draw(cpu.X)
        pixels.append(pixel)
        cpu.run()
        cycle += 1
    
    print(signal_strengths)
    print(f"The sum of signal strengths is: {sum(signal_strengths)}")

    print("-"*20)
    screen_width = 40
    for i in range(6):
        print("".join(pixels[screen_width*i:screen_width*(i+1)]))

