import dataclasses
import itertools
from typing import Self

import numpy as np

from utils import AOC


class Day11(AOC.GridAOC):
    DAY = 11

    def part_1(self):
        return sum(self.get_galaxies_distance(expansion_factor=2))

    def part_2(self):
        return sum(self.get_galaxies_distance(expansion_factor=1_000_000))

    def get_galaxies_distance(self, expansion_factor):
        empty_rows, empty_cols = self.get_empty(self.input)

        galaxies = [self.Galaxy(a, b) for a, b in zip(*np.where(self.input == "#"))]
        return [
            a.distance(b, empty_rows, empty_cols, expansion_factor=expansion_factor)
            for a, b in itertools.combinations(galaxies, 2)
        ]

    @dataclasses.dataclass
    class Galaxy:
        y: int
        x: int

        def distance(self, other: Self, empty_rows, empty_cols, expansion_factor):
            min_x, max_x = sorted((self.x, other.x))
            min_y, max_y = sorted((self.y, other.y))
            count_empty_cols = len(
                list(filter(lambda x: min_x < x < max_x, empty_cols))
            )
            count_empty_rows = len(
                list(filter(lambda y: min_y < y < max_y, empty_rows))
            )

            return (
                abs(self.x - other.x)
                + abs(self.y - other.y)
                + (count_empty_rows + count_empty_cols) * (expansion_factor - 1)
            )

    @staticmethod
    def get_empty(array):
        def get_empty_lines(array):
            height, _ = array.shape
            empty_lines = []
            for i in range(height):
                if all(array[i, :] == "."):
                    empty_lines.append(i)

            return empty_lines

        rows = get_empty_lines(array)
        cols = get_empty_lines(array.transpose())

        return rows, cols


if __name__ == "__main__":
    day_11 = Day11()
    print(day_11.part_2())
