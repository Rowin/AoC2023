import dataclasses
from collections import defaultdict
from typing import Literal

import numpy as np

from utils import AOC


type Direction = Literal["up", "down", "left", "right"]


class Day16(AOC.GridAOC):
    DAY = 16

    @dataclasses.dataclass
    class Beam:
        heading: Direction
        position: tuple

    mirrors = {
        "/": {
            "left": "down",
            "down": "left",
            "up": "right",
            "right": "up",
        },
        "\\": {
            "left": "up",
            "down": "right",
            "up": "left",
            "right": "down",
        },
    }

    @staticmethod
    def get_next_position(position, direction):
        y, x = position
        match direction:
            case "left":
                return y, x - 1
            case "right":
                return y, x + 1
            case "up":
                return y - 1, x
            case "down":
                return y + 1, x

    def find_powered_cells(self, starting_beam):
        grid = np.pad(self.input, pad_width=1, mode="constant", constant_values="0")
        beams = [starting_beam]  # Beware of the padding!

        visited_tiles = defaultdict(list)
        while len(beams) > 0:
            next_beams = []
            for beam in beams:
                if beam.heading in visited_tiles[beam.position]:
                    continue
                if grid[beam.position] == "0":
                    continue

                cell = grid[beam.position]
                visited_tiles[beam.position].append(beam.heading)
                next_directions: [Direction]
                match cell:
                    case "/" | "\\":
                        next_directions = [self.mirrors[cell][beam.heading]]
                    case "-":
                        if beam.heading in ("up", "down"):
                            next_directions = ["left", "right"]
                        else:
                            next_directions = [beam.heading]
                    case "|":
                        if beam.heading in ("left", "right"):
                            next_directions = ["up", "down"]
                        else:
                            next_directions = [beam.heading]
                    case _:
                        next_directions = [beam.heading]

                for next_direction in next_directions:
                    next_beams.append(
                        self.Beam(
                            next_direction,
                            self.get_next_position(beam.position, next_direction),
                        )
                    )

            beams = next_beams

        return len(list(filter(lambda v: len(v) > 0, visited_tiles.values())))

    def part_1(self):
        starting_beam = self.Beam("right", (1, 1))
        return self.find_powered_cells(starting_beam)

    def part_2(self):
        height, width = self.input.shape

        top_beams = [self.Beam("down", (1, i + 1)) for i in range(width)]
        bottom_beams = [self.Beam("up", (height, i + 1)) for i in range(width)]
        left_beams = [self.Beam("right", (i + 1, 1)) for i in range(height)]
        right_beams = [self.Beam("left", (i + 1, width)) for i in range(height)]

        return max(
            [
                self.find_powered_cells(beam)
                for beam in top_beams + bottom_beams + left_beams + right_beams
            ]
        )


if __name__ == "__main__":
    day_16 = Day16()
    print(day_16.part_2())
