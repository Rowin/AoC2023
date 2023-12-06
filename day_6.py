import math

import AOC


class Day6(AOC.LinearAOC):
    DAY = 6

    @staticmethod
    def get_possible_records(d, r):
        delta = (d**2 - 4 * r) ** 0.5 - 10e-14  # Small offset if delta integer
        return math.floor((d + delta) * 0.5) - math.ceil((d - delta) * 0.5) + 1

    def part_1(self):
        times = map(int, self.input[0].split(":")[1].split())
        records = map(int, self.input[1].split(":")[1].split())

        possible_records = [
            self.get_possible_records(d, r) for d, r in zip(times, records)
        ]

        return math.prod(possible_records)

    def part_2(self):
        time = int("".join(self.input[0].split(":")[1].split()))
        record = int("".join(self.input[1].split(":")[1].split()))

        return self.get_possible_records(time, record)


if __name__ == "__main__":
    day_6 = Day6()
    print(day_6.part_2())
