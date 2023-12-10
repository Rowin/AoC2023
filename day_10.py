import enum

import numpy as np

import AOC


class Day10(AOC.GridAOC):
    DAY = 10

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
        starting_position = np.array((*a, *b))
        y_s, x_s = starting_position

        # Search for first pipe
        if self.input[starting_position + self.Directions.NORTH] in ("|", "F", "7"):
            position = starting_position + self.Directions.NORTH
            origin = self.Directions.SOUTH
        elif self.input[starting_position + self.Directions.SOUTH] in ("|", "J", "L"):
            position = starting_position + self.Directions.SOUTH
            origin = self.Directions.NORTH
        elif self.input[starting_position + self.Directions.WEST] in ("-", "L", "F"):
            position = starting_position + self.Directions.WEST
            origin = self.Directions.EAST
        elif self.input[starting_position + self.Directions.EAST] in ("-", "J", "7"):
            position = starting_position + self.Directions.EAST
            origin = self.Directions.WEST

        while position != starting_position:
            pipe = self.input(position)
            (destination,) = [
                direction for direction in self.PIPES[pipe] if direction != origin
            ]

            if destination == self.Directions.NORTH:
                origin = self.Directions.SOUTH
            elif destination == self.Directions.SOUTH:
                origin = self.Directions.NORTH
            elif destination == self.Directions.EAST:
                origin = self.Directions.WEST
            elif destination == self.Directions.WEST:
                origin = self.Directions.EAST

            position += destination


if __name__ == "__main__":
    day_10 = Day10()
    print(day_10.part_1())
