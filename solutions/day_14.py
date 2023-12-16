import numpy as np
import numpy.typing as npt

from tqdm import tqdm

from utils import AOC


class Day14(AOC.GridAOC):
    DAY = 14

    def part_1(self):
        return self.weight(np.rot90(self.roll_west(np.rot90(self.input)), -1))

    def part_2(self):
        platform = self.input
        for i in tqdm(range(1_000)):
            platform = self.cycle(platform)

        return self.weight(platform)

    def cycle(self, platform):
        platform = self.roll_west(np.rot90(platform))
        platform = self.roll_west(np.rot90(platform, -1))
        platform = self.roll_west(np.rot90(platform, -1))
        platform = self.roll_west(np.rot90(platform, -1))
        return np.rot90(platform, 2)

    @staticmethod
    def weight(platform):
        height, width = platform.shape

        total_weight = 0
        for i, line in enumerate(platform):
            total_weight += sum(line == "O") * (height - i)

        return total_weight

    @staticmethod
    def roll_west(platform):
        def compute_row(row: npt.NDArray) -> []:
            segments = "".join(row).split("#")

            new_segments = []
            for segment in segments:
                round_stone = segment.count("O")
                new_segment = "O" * round_stone + "." * (len(segment) - round_stone)
                new_segments.append(new_segment)

            return list("#".join(new_segments))

        return np.array([compute_row(line) for line in platform])


if __name__ == "__main__":
    day_14 = Day14()
    print(day_14.part_2())
