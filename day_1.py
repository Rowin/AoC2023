import re

from AOC import LinearAOC


class Day1(LinearAOC):
    DAY = 1

    def part_1(self):
        calib_values = 0
        for line in self.input:
            digits = [d for d in line if d.isdigit()]
            calib_value = int(digits[0] + digits[-1])
            calib_values += calib_value

        return calib_values

    def part_2(self):
        spelled_digits = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }

        calib_values = 0
        group = f'{"|".join(spelled_digits)}|\\d'
        for line in self.input:
            leftmost = re.match(f"^.*?({group})", line).group(1)
            rightmost = re.match(f".*({group}).*$", line).group(1)

            leftmost = spelled_digits.get(leftmost, leftmost)
            rightmost = spelled_digits.get(rightmost, rightmost)

            calib_value = int(leftmost + rightmost)
            calib_values += calib_value

        return calib_values


if __name__ == "__main__":
    problem = Day1()
    print(problem.part_1())
    print(problem.part_2())
