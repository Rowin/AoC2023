import functools
import re


import AOC


class Day12(AOC.LinearAOC):
    DAY = 12

    def part_1(self):
        counter = 0
        for line in self.input:
            springs, status_record = line.split(" ")
            status_record = tuple(map(int, status_record.split(",")))

            counter += self.possible_springs(springs, status_record)

        return counter

    @functools.lru_cache(maxsize=None)
    def possible_springs(self, springs: str, records):
        if len(records) == 0:
            if "#" in springs:
                return 0
            else:
                return 1

        if len(springs) == 0:
            if len(records) > 0:
                return 0
            else:
                return 1

        first_spring = springs[0]
        if first_spring == ".":
            return self.possible_springs(springs[1:], records)
        elif first_spring == "#":
            if m := re.match("(#+)\\.(.*)", springs):
                if len(m.group(1)) == records[0]:
                    return self.possible_springs(m.group(2), records[1:])
                else:
                    return 0

        if "?" in springs:
            return self.possible_springs(
                springs.replace("?", ".", 1), records
            ) + self.possible_springs(springs.replace("?", "#", 1), records)

        if tuple(map(len, springs.replace(".", " ").split())) == records:
            # print(springs, records)
            return 1

        print(springs, records)
        return 0

    def part_2(self):
        ...


if __name__ == "__main__":
    day_12 = Day12()
    print(day_12.part_1())
