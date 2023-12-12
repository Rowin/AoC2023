import collections
import math

from utils import AOC


class Day2(AOC.LinearAOC):
    DAY = 2

    def part_1(self):
        objectives = {"red": 12, "green": 13, "blue": 14}

        acc = 0
        for game_id, line in enumerate(self.input, start=1):
            records = line.split(": ")[1].split("; ")

            compatibility = []
            for record in records:
                for color in record.split(", "):
                    number_of_cubes, cubes_color = color.split(" ")
                    compatibility.append(
                        int(number_of_cubes) <= objectives[cubes_color]
                    )

            if all(compatibility):
                acc += game_id

        return acc

    def part_2(self):
        acc = 0
        for line in self.input:
            counter = collections.defaultdict(list)
            records = line.split(": ")[1].split("; ")

            for record in records:
                for color in record.split(", "):
                    number_of_cubes, cubes_color = color.split(" ")
                    counter[cubes_color].append(int(number_of_cubes))

            power = math.prod([max(i) for i in counter.values()])
            acc += power

        return acc


if __name__ == "__main__":
    day_2 = Day2()
    print(day_2.part_2())
