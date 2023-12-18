from dataclasses import dataclass, astuple
import enum

import numpy as np

from utils import AOC


@dataclass
class Point:
    y: int
    x: int

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)


class Day10(AOC.GridAOC):
    DAY = 10

    PIPES = {
        "|": {"down": "down", "up": "up"},
        "-": {"left": "left", "right": "right"},
        "L": {"down": "right", "left": "up"},
        "J": {"down": "left", "right": "up"},
        "7": {"up": "left", "right": "down"},
        "F": {"up": "right", "left": "down"},
    }

    DIRECTIONS = {
        "left": Point(0, -1),
        "right": Point(0, 1),
        "up": Point(-1, 0),
        "down": Point(1, 0),
    }

    def get_point(self, point: Point):
        return self.input[astuple(point)]

    def get_boundaries(self):
        starting_point = Point(*next(zip(*np.where(self.input == "S"))))

        if self.get_point(starting_point + self.DIRECTIONS["up"]) in ("F", "7"):
            heading = "up"
        elif self.get_point(starting_point + self.DIRECTIONS["down"]) in ("J", "L"):
            heading = "down"
        elif self.get_point(starting_point + self.DIRECTIONS["left"]) in ("F", "L"):
            heading = "left"
        elif self.get_point(starting_point + self.DIRECTIONS["right"]) in ("J", "7"):
            heading = "right"

        current_point = starting_point + self.DIRECTIONS[heading]
        loop_pipes = [starting_point]

        while True:
            loop_pipes.append(current_point)
            pipe = self.get_point(current_point)
            heading = self.PIPES[pipe][heading]

            current_point += self.DIRECTIONS[heading]

            if current_point == starting_point:
                break

        return loop_pipes

    @staticmethod
    def shoelace_area(vertices):  # Shoelace formula
        total = 0
        for a, b in zip(vertices, vertices[1:]):
            total += a.x * b.y - a.y * b.x

        return abs(total // 2)

    def part_1(self):
        return len(self.get_boundaries()) // 2

    def part_2(self):
        boundaries = self.get_boundaries()

        vertices = [
            position
            for position in boundaries
            if self.get_point(position) in ("F", "7", "L", "J")
        ]

        vertices.append(vertices[0])

        area = self.shoelace_area(vertices)

        return area + 1 - len(boundaries) // 2  # Pick's theorem


if __name__ == "__main__":
    day_10 = Day10()
    print(day_10.part_2())
