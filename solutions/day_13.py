import numpy.typing as npt

from utils import AOC


def matrix_to_int(matrix: npt.NDArray):
    height, width = matrix.shape

    rows = [
        int("".join(matrix[i, :]).replace("#", "1").replace(".", "0"), base=2)
        for i in range(height)
    ]

    cols = [
        int("".join(matrix[:, i]).replace("#", "1").replace(".", "0"), base=2)
        for i in range(width)
    ]

    return rows, cols


class Day13(AOC.GridGroupAOC):
    DAY = 13

    def part_1(self):
        count = 0
        for matrix in self.input:
            rows, cols = matrix_to_int(matrix)

            for index in range(len(rows)):
                diff = [
                    (a ^ b).bit_count()
                    for a, b in zip(rows[index:], reversed(rows[:index]))
                ]
                count += (sum(diff) == 0) * index * 100

            for index in range(len(cols)):
                diff = [
                    (a ^ b).bit_count()
                    for a, b in zip(cols[index:], reversed(cols[:index]))
                ]
                count += (sum(diff) == 0) * index

        return count

    def part_2(self):
        count = 0
        for matrix in self.input:
            rows, cols = matrix_to_int(matrix)

            for index in range(len(rows)):
                diff = [
                    (a ^ b).bit_count()
                    for a, b in zip(rows[index:], reversed(rows[:index]))
                ]
                count += (sum(diff) == 1) * index * 100

            for index in range(len(cols)):
                diff = [
                    (a ^ b).bit_count()
                    for a, b in zip(cols[index:], reversed(cols[:index]))
                ]
                count += (sum(diff) == 1) * index

        return count


if __name__ == "__main__":
    day_13 = Day13()
    print(day_13.part_2())
