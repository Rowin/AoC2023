import dataclasses
import queue
from typing import Self

from utils import AOC


@dataclasses.dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Self):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int):
        return Point(other * self.x, other * self.y)

    def distance(self, other: Self):
        return abs(self.x - other.x) + abs(self.y - other.y)


DIRECTIONS = {"R": Point(1, 0), "D": Point(0, 1), "L": Point(-1, 0), "U": Point(0, -1)}


class Day18(AOC.LinearAOC):
    DAY = 18

    @staticmethod
    def get_boundaries_count(vertices: [Point]):
        return sum([a.distance(b) for a, b in zip(vertices, vertices[1:])])

    def get_vertices(self, from_color=False):
        current_position = Point(0, 0)
        vertices: [Point] = [current_position]
        for line in self.input:
            direction, length, color = line.split()
            if from_color:
                length = int(color[2:7], base=16)
                direction = list(DIRECTIONS.keys())[int(color[7])]

            current_position += DIRECTIONS[direction] * int(length)
            vertices.append(current_position)

        return vertices

    @staticmethod
    def shoelace_area(vertices):  # Shoelace formula
        total = 0
        for a, b in zip(vertices, vertices[1:]):
            total += a.x * b.y - a.y * b.x

        return total // 2

    def part_1(self):
        vertices = self.get_vertices()
        boundaries = self.get_boundaries_count(vertices)

        return self.shoelace_area(vertices) + 1 + boundaries // 2  # Pick's theorem

    def part_2(self):
        vertices = self.get_vertices(from_color=True)
        boundaries = self.get_boundaries_count(vertices)

        return self.shoelace_area(vertices) + 1 + boundaries // 2  # Pick's theorem


if __name__ == "__main__":
    day_18 = Day18()
    print(day_18.part_2())
