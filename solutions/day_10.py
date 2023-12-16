import dataclasses
import enum

import numpy as np

from utils import AOC


class Day10(AOC.GridAOC):
    DAY = 10

    @dataclasses.dataclass
    class Point:
        x: int
        y: int

        def neighbor(self, direction):
            return self.__class__(self.x + direction[0], self.y + direction[1])

        @property
        def west(self):
            return self.neighbor([-1, 0])

        @property
        def east(self):
            return self.neighbor(Day10.Directions.EAST)

        @property
        def north(self):
            return self.neighbor(Day10.Directions.NORTH)

        @property
        def south(self):
            return self.neighbor(Day10.Directions.SOUTH)

    class Directions(enum.Enum):
        NORTH = np.array((-1, 0))
        SOUTH = np.array((1, 0))
        EAST = np.array((0, 1))
        WEST = np.array((0, -1))

    PIPES = {
        "-": [Directions.EAST, Directions.WEST],
        "|": [Directions.SOUTH, Directions.NORTH],
        "J": [Directions.WEST, Directions.NORTH],
        "L": [Directions.EAST, Directions.NORTH],
        "7": [Directions.WEST, Directions.SOUTH],
        "F": [Directions.EAST, Directions.SOUTH],
    }

    def part_1(self):
        a, b = np.where(self.input == "S")
        starting_position = self.Point(np.array((*a, *b)))

        position = starting_position.north()


if __name__ == "__main__":
    day_10 = Day10()
    print(day_10.part_1())
