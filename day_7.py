import collections
import enum
import functools

import AOC


class Day7(AOC.LinearAOC):
    DAY = 7

    @functools.total_ordering
    class Hand:
        def __init__(self, raw_hand, jokers=False):
            hand, bid = raw_hand.split()
            self.bid = int(bid)
            self.hand: str = hand
            self.type = self.compute_type()

            if jokers:
                self.type = self.apply_jokers()

            self.score = self.compute_score(jokers=jokers)

        class Type(enum.IntEnum):
            FIVE_OF_A_KIND = 7
            FOUR_OF_A_KIND = 6
            FULL_HOUSE = 5
            THREE_OF_A_KIND = 4
            TWO_PAIR = 3
            ONE_PAIR = 2
            HIGH_CARD = 1

        def compute_type(self):
            counter = collections.Counter(self.hand)
            match sorted(counter.values()):
                case 5,:
                    return self.Type.FIVE_OF_A_KIND
                case 1, 4:
                    return self.Type.FOUR_OF_A_KIND
                case 2, 3:
                    return self.Type.FULL_HOUSE
                case 1, 1, 3:
                    return self.Type.THREE_OF_A_KIND
                case 1, 2, 2:
                    return self.Type.TWO_PAIR
                case 1, 1, 1, 2:
                    return self.Type.ONE_PAIR
                case 1, 1, 1, 1, 1:
                    return self.Type.HIGH_CARD
                case _:
                    raise

        def compute_score(self, jokers):
            if jokers:
                translate_to = '23456789A1CDE'
            else:
                translate_to = '23456789ABCDE'

            score = int(
                f'{self.type}{self.hand.translate(str.maketrans("23456789TJQKA", translate_to))}',
                16,
            )

            return score

        def apply_jokers(self):
            if "J" not in self.hand:
                return self.type

            match self.type:
                case self.Type.HIGH_CARD:
                    return self.Type.ONE_PAIR
                case self.Type.ONE_PAIR:
                    return self.Type.THREE_OF_A_KIND
                case self.Type.THREE_OF_A_KIND:
                    return self.Type.FOUR_OF_A_KIND
                case self.Type.FULL_HOUSE:
                    return self.Type.FIVE_OF_A_KIND
                case self.Type.FOUR_OF_A_KIND:
                    return self.Type.FIVE_OF_A_KIND
                case self.Type.TWO_PAIR:
                    if self.hand.count("J") == 1:
                        return self.Type.FULL_HOUSE
                    else:
                        return self.Type.FOUR_OF_A_KIND
                case _:
                    return self.type

        def __lt__(self, other):
            return self.score < other.score

        def __eq__(self, other):
            return self.score == other.score

        def __repr__(self):
            return f"{self.hand} {self.bid} {self.score}"

    def part_1(self):
        hands = sorted([self.Hand(hand) for hand in self.input])
        winnings = [rank * hand.bid for rank, hand in enumerate(hands, start=1)]

        return sum(winnings)

    def part_2(self):
        hands = sorted([self.Hand(hand, jokers=True) for hand in self.input])
        winnings = [rank * hand.bid for rank, hand in enumerate(hands, start=1)]

        return sum(winnings)


if __name__ == "__main__":
    day_7 = Day7()
    print(day_7.part_2())
