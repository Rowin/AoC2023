import dataclasses
import functools
from typing import List, Iterable
import matplotlib.pyplot as plt

import numpy as np

from utils import AOC


@dataclasses.dataclass
class Position:
    y: int
    x: int

    def __add__(self, other: Iterable):
        if isinstance(other, tuple):
            other = Position(*other)
        return Position(self.y + other.y, self.x + other.x)

    def __hash__(self):
        return (self.y, self.x).__hash__()

    def as_tuple(self):
        return self.y, self.x


class Day21(AOC.GridAOC):
    DAY = 21

    def part_1(self):
        self.garden = np.pad(
            self.input, pad_width=1, mode="constant", constant_values="#"
        )
        starting_position = Position(*next(zip(*np.where(self.garden == "S"))))

        possible_positions = {starting_position}
        for step in range(64):
            next_possible_positions: set[Position] = set()
            for position in possible_positions:
                next_possible_positions.update(self.get_neighbor_garden_patch(position))

            possible_positions = next_possible_positions

        return len(possible_positions)

    def part_2(self):
        self.garden = np.concatenate([np.concatenate([self.input] * 9, 1)] * 9, 0)

        starting_position = Position(*next(zip(*np.where(self.input == "S"))))

        height, width = self.input.shape
        starting_position += Position(4 * height, 4 * width)

        len_history = []
        possible_positions = {starting_position}
        for step in range(520):
            next_possible_positions: List[Position] = []
            try:
                for position in possible_positions:
                    next_possible_positions += self.get_neighbor_garden_patch(position)
            except:
                break

            possible_positions = set(next_possible_positions)
            len_history.append(len(possible_positions))

        plt.plot(list(range(len(len_history))), len_history, ".")
        print(len_history)
        plt.show()

    @functools.lru_cache(maxsize=None)
    def get_neighbor_garden_patch(self, position: Position) -> List:
        neighbors = []
        for movement in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            candidate_neighbor = position + movement
            if self.garden[candidate_neighbor.as_tuple()] in (".", "S"):
                neighbors.append(candidate_neighbor)

        return neighbors


if __name__ == "__main__":
    day_21 = Day21()
    print(day_21.part_2())
