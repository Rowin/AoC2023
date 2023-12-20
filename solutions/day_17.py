from collections import defaultdict

import math

from utils import AOC


class Day17(AOC.GridAOC):
    DAY = 17

    def part_1(self):
        distances = defaultdict(lambda: math.inf)

        distances[(0, 0)] = 0
        visited_nodes = set()

        end_node = self.input.shape
        while end_node not in visited_nodes:
            min()

        ...

    def part_2(self):
        pass

    @staticmethod
    def get_neighbors(position):
        a, b = position

        return [
            (a - 1, b),
            (a + 1, b),
            (a, b - 1),
            (a, b + 1),
        ]


if __name__ == "__main__":
    day_17 = Day17()
    print(day_17.part_1())
