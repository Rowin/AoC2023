import collections
import re

import numpy as np

import AOC


class Day3(AOC.GridAOC):
    DAY = 3

    def __init__(self):
        super().__init__()

        self.schematic = np.pad(self.input, pad_width=1, constant_values=".")
        _, self.width = self.schematic.shape

    def part_1(self):
        schematic = self.schematic
        width = self.width

        part_numbers = []
        for match in re.finditer("(\\d+)", "".join(schematic.flatten())):
            number = int(match.group())
            s = match.start()
            e = match.end()

            neighbors = np.concatenate(
                (
                    schematic.flat[s - (width + 1) : e - (width - 1)],
                    schematic.flat[s + (width - 1) : e + (width + 1)],
                    [schematic.flat[s - 1]],
                    [schematic.flat[e]],
                )
            )

            if any(
                [not (neighbor.isalpha() or neighbor == ".") for neighbor in neighbors]
            ):
                part_numbers.append(number)

        return sum(part_numbers)

    def find_gear_position(self, start: int, end: int = None):
        if end is None:
            neighbors = [self.schematic.flat[start]]
        else:
            neighbors = self.schematic.flat[start:end]

        pseudo_gears = []
        for position, neighbor in enumerate(neighbors, start=start):
            if neighbor == "*":
                pseudo_gears.append(position)

        return pseudo_gears

    def part_2(self):
        schematic = self.schematic
        width = self.width

        candidate_gears = collections.defaultdict(list)
        gear_ratios = []
        for match in re.finditer("(\\d+)", "".join(schematic.flatten())):
            number = int(match.group())
            s = match.start()
            e = match.end()

            pseudo_gears = (
                self.find_gear_position(s - (width + 1), e - (width - 1))
                + self.find_gear_position(s + (width - 1), e + (width + 1))
                + self.find_gear_position(s - 1)
                + self.find_gear_position(e)
            )

            for gear in pseudo_gears:
                candidate_gears[gear].append(number)

        for candidate_gear, neighbors in candidate_gears.items():
            if len(neighbors) == 2:
                gear_ratios.append(neighbors[0] * neighbors[1])

        return sum(gear_ratios)


if __name__ == "__main__":
    day3 = Day3()
    print(day3.part_2())
