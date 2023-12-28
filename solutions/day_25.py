import collections

from utils import AOC


class Graph:
    def __init__(self):
        self.graph = collections.defaultdict(list)

    def add_edge(self, a, b):
        self.graph[a].append(b)
        self.graph[b].append(a)

    def remove_edge(self, a, b):
        self.graph[a].remove(b)
        self.graph[b].remove(a)


class Day25(AOC.LinearAOC):
    DAY = 25

    def part_1(self):
        graph = Graph()
        for line in self.input:
            a, components = line.split(": ")
            for component in components.split(" "):
                graph.add_edge(a, component)

        # Find these nodes through visualisation...
        graph.remove_edge("ttv", "ztc")
        graph.remove_edge("vfh", "bdj")
        graph.remove_edge("rpd", "bnv")

        visited = []

        def color_fill(_from):
            if _from in visited:
                return

            else:
                visited.append(_from)
                for neighbor in graph.graph[_from]:
                    color_fill(neighbor)

        color_fill("ttv")
        return (len(graph.graph) - len(visited)) * len(visited)

    def part_2(self):
        raise NotImplemented("It's day 25, no part 2!")


if __name__ == "__main__":
    day_25 = Day25()
    print(day_25.part_1())
