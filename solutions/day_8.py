import dataclasses
import itertools
import math
import re
from collections import defaultdict

from utils import AOC


class Day8(AOC.LineGroupAOC):
    DAY = 8

    @dataclasses.dataclass
    class Node:
        starting: bool = False
        ending: bool = False
        name: str = ""
        left = None
        right = None

        def __repr__(self):
            return self.name

    def get_nodes(self):
        nodes = self.input[1]
        nodes_dict = defaultdict(self.Node)
        for raw_node in nodes:
            node, left, right = re.match(
                r"(\w{3}) = \((\w{3}), (\w{3})\)", raw_node
            ).groups()

            nodes_dict[node].name = node
            nodes_dict[node].left = nodes_dict[left]
            nodes_dict[node].right = nodes_dict[right]

            if node.endswith("A"):
                nodes_dict[node].starting = True
            elif node.endswith("Z"):
                nodes_dict[node].ending = True

        return nodes_dict

    def get_loop_size(self, node):
        instructions = self.input[0][0]

        nodes_dict = self.nodes

        current_node = nodes_dict[node]
        counter = 0
        for instruction in itertools.cycle(instructions):
            counter += 1
            if instruction == "L":
                current_node = current_node.left
            elif instruction == "R":
                current_node = current_node.right

            if current_node.ending:
                break

        return counter

    def part_1(self):
        self.nodes = self.get_nodes()

        return self.get_loop_size("AAA")

    def part_2(self):
        self.nodes = self.get_nodes()
        loops_sizes = [
            self.get_loop_size(node.name)
            for node in self.nodes.values()
            if node.starting
        ]
        return math.lcm(*loops_sizes)


if __name__ == "__main__":
    day_8 = Day8()
    print(day_8.part_2())
