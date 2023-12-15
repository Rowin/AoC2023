import re
from collections import defaultdict

from utils import AOC


class Day15(AOC.LinearAOC):
    DAY = 15

    def part_1(self):
        initialization_seq = self.input[0].split(",")
        return sum([self.hash(step) for step in initialization_seq])

    def part_2(self):
        initialization_seq = self.input[0].split(",")
        boxes = defaultdict(self.Box)
        for step in initialization_seq:
            label, sep, focal_length = re.match(r"([a-z]+)([-=])(\d?)", step).groups()

            box = boxes[self.hash(label)]
            if sep == "=":
                box.add_lens(label, int(focal_length))
            elif sep == "-":
                box.remove_lens(label)

        return self.focusing_power(boxes)

    class Box:
        def __init__(self):
            self.lenses = dict()

        def add_lens(self, label: str, focal_length: int) -> None:
            # Dicts are ordered from 3.7!
            self.lenses[label] = focal_length

        def remove_lens(self, label: str) -> None:
            try:
                del self.lenses[label]
            except KeyError:
                pass

        def local_power(self) -> int:
            return sum(
                [
                    focal_length * position
                    for position, focal_length in enumerate(
                        self.lenses.values(), start=1
                    )
                ]
            )

    @staticmethod
    def hash(string: str) -> int:
        current = 0

        for char in string:
            current += ord(char)
            current *= 17
            current %= 256

        return current

    @staticmethod
    def focusing_power(boxes):
        return sum(
            [(box_label + 1) * box.local_power() for box_label, box in boxes.items()]
        )


if __name__ == "__main__":
    day_15 = Day15()
    print(day_15.part_2())
