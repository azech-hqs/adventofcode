import sys
from typing import List, Optional
from anytree import Node, RenderTree
from anytree.resolver import Resolver
from anytree import search


DISK_SPACE = 70000000
FREE_REQUIRED = 30000000

class Command:
    def __init__(self, command: str, output: Optional[List[str]] = None) -> None:
        cmd_split = command.rstrip("\n").split(" ")
        self.command = cmd_split[0]
        self.target = "" if len(cmd_split) == 1 else cmd_split[1]
        if output:
            self.output = [o.split(" ") for o in output]

    @classmethod
    def from_block(cls, command_block: str):
        c = list(filter(None, command_block.rstrip("\n").split("\n")))
        if len(c) == 1:
            return cls(command=c[0])
        else:
            return cls(command=c[0], output=c[1:])
    

def build_tree(command_blocks: List[str]):
    root = FS_Node("root", is_directory=True)
    r = Resolver("name")

    current_node = r.get(root, ".")
    for block in command_blocks:
        cmd = Command.from_block(block)
        match cmd.command:
            case "cd":
                current_node = current_node.change_directory(cmd.target, resolver=r)
            case "ls":
                [current_node.add_item(o) for o in cmd.output]
    # print(RenderTree(root))
    return root


class FS_Node(Node):
    def __init__(self,
            name: str,
            size: int = 0,
            is_directory: Optional[bool] = False,
            **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.size = size
        self.is_directory = is_directory

    def change_directory(self, path: str, resolver: Resolver) -> "FS_Node":
        if path == "/":
            return resolver.get(self, f"/root")
        return resolver.get(self, path)

    def add_item(self, dir_item: List[str]) -> None:
        names = list(map(lambda x: x.name, self.children))
        match dir_item:
            case ["dir", dirname]:
                if dirname not in names:
                    FS_Node(name=dirname, is_directory=True, parent=self)
            case [size, filename]:
                if filename not in names:
                    FS_Node(name=filename, size=int(size), parent=self)
    
    @property
    def disk_usage(self) -> int:
        if not self.is_directory:
            return self.size
        return sum(list(map(lambda x: x.disk_usage, self.children)))


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        content = f.read()

    command_blocks = list(filter(None, content.split("$ ")))
    file_tree = build_tree(command_blocks)
    medium = search.findall(file_tree, lambda node: (node.disk_usage <= 100000) and node.is_directory)
    print(f"TOTAL: {sum([d.disk_usage for d in medium])}")

    total_used = file_tree.disk_usage
    to_be_freed = FREE_REQUIRED - DISK_SPACE + total_used
    print(f"total unused space = {DISK_SPACE - total_used}")
    print(f"disk space to be freed = {to_be_freed}")

    to_be_deleted = search.findall(file_tree, lambda node: (node.disk_usage >= to_be_freed) and node.is_directory)
    to_be_deleted = sorted(to_be_deleted, key=lambda x: x.disk_usage)
    print(f"delete: {to_be_deleted[0]} (size={to_be_deleted[0].disk_usage})")
