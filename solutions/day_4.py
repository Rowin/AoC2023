from utils import AOC


class Day4(AOC.LinearAOC):
    DAY = 4

    @staticmethod
    def get_number_of_winning_cards(line):
        _, numbers = line.split(": ")
        winning_numbers, numbers_you_have = numbers.split(" | ")
        winning_numbers = set(winning_numbers.split())
        numbers_you_have = set(numbers_you_have.split())

        common_numbers = winning_numbers & numbers_you_have
        return len(common_numbers)

    def part_1(self):
        scores = []
        for line in self.input:
            number_of_winning_card = self.get_number_of_winning_cards(line)
            if number_of_winning_card > 0:
                scores.append(2 ** (number_of_winning_card - 1))

        return sum(scores)

    def part_2(self):
        max_card_id = len(self.input)
        cards_set = [1] * max_card_id
        for s, line in enumerate(self.input, start=1):
            number_of_winning_card = self.get_number_of_winning_cards(line)
            for card_id in range(s + 1, s + 1 + number_of_winning_card):
                if card_id <= max_card_id:
                    cards_set[card_id - 1] += cards_set[s - 1]

        return sum(cards_set)


if __name__ == "__main__":
    day_4 = Day4()
    print(day_4.part_2())
