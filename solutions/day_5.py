from utils import AOC


class Day5(AOC.LineGroupAOC):
    DAY = 5

    @staticmethod
    def get_destination(source, _map):
        header = _map[0]
        for _range in _map[1:]:
            destination_start, source_start, range_length = map(int, _range.split())
            if source in range(source_start, source_start + range_length):
                return source - source_start + destination_start
        else:
            return source

    def get_locations(self, seeds):
        locations = []
        for seed in seeds:
            source = seed
            for _map in self.input[1:]:
                destination = self.get_destination(source, _map)
                source = destination

            locations.append(destination)

        return min(locations)

    def part_1(self):
        seeds = map(int, self.input[0][0].split(": ")[1].split())

        return self.get_locations(seeds)

    def part_2(self):
        seeds = list(map(int, self.input[0][0].split(": ")[1].split()))

        return sum(seeds[1::2])
        # expanded_seeds = []
        # for i in range(len(seeds) // 2):
        #     start = seeds[2 * i]
        #     length = seeds[2 * i + 1]
        #     expanded_seeds.append(range(start, start + length))
        #
        # return len(list(itertools.chain.from_iterable(expanded_seeds)))


if __name__ == "__main__":
    day_5 = Day5()
    print(day_5.part_1())
