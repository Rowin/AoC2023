import functools
import re

from utils import AOC


class Day12(AOC.LinearAOC):
    DAY = 12

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
            m = re.match(r"(#+)(\.|\?|$)(.*)", springs)
            group, sep, end = m.groups()
            if len(group) > records[0]:
                return 0
            elif len(group) == records[0]:
                if sep == "?":
                    return self.possible_springs(f"{group}.{end}", records)
                else:
                    return self.possible_springs(end, records[1:])
            else:
                if sep == "?":
                    return self.possible_springs(f"{group}#{end}", records)
                else:
                    return 0
        elif first_spring == "?":
            return self.possible_springs(
                springs.replace("?", ".", 1), records
            ) + self.possible_springs(springs.replace("?", "#", 1), records)

    def part_1(self):
        counter = 0
        for line in self.input:
            springs, status_record = line.split(" ")
            status_record = tuple(map(int, status_record.split(",")))

            counter += self.possible_springs(springs, status_record)

        return counter

    def part_2(self):
        counter = 0
        for line in self.input:
            springs, status_record = line.split(" ")
            springs = "?".join([springs] * 5)
            status_record = tuple(map(int, status_record.split(",") * 5))

            counter += self.possible_springs(springs, status_record)

        return counter


if __name__ == "__main__":
    day_12 = Day12()
    print(day_12.part_2())
