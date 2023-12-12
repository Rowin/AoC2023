import numpy as np

from utils import AOC


class Day9(AOC.LinearAOC):
    DAY = 9

    def polynomia(self, history):
        tmp_history = history
        n = 0
        while not all([reading == 0 for reading in tmp_history]):
            tmp_history = [b - a for a, b in zip(tmp_history, tmp_history[1:])]
            n += 1

        poly = np.polynomial.Polynomial.fit(range(len(history)), history, n)

        return poly

    def part_1(self):
        extrapolated_values = []
        for line in self.input:
            history = list(map(int, line.split()))
            poly = self.polynomia(history)
            extrapolated_values.append(poly(len(history)))

        return round(sum(extrapolated_values))

    def part_2(self):
        extrapolated_values = []
        for line in self.input:
            history = list(map(int, line.split()))
            poly = self.polynomia(history)
            extrapolated_values.append(poly(-1))

        return round(sum(extrapolated_values))


if __name__ == "__main__":
    day_9 = Day9()
    print(day_9.part_2())
