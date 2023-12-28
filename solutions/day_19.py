import collections
import dataclasses
import operator
import queue
import re
from typing import Union, List, Dict, NamedTuple
import math

from utils import AOC


class PartRatings(NamedTuple):
    x: int
    m: int
    a: int
    s: int


@dataclasses.dataclass
class Range:
    start: int
    stop: int

    def __contains__(self, item):
        return self.start <= item <= self.stop

    def __lt__(self, other: int):
        return self.stop < other

    def __gt__(self, other: int):
        return self.start > other

    def __len__(self):
        return self.stop - self.start + 1


class RangeRatings(NamedTuple):
    x: Range
    m: Range
    a: Range
    s: Range


SimpleRule = collections.namedtuple("SimpleRule", ["destination"])

ComparisonRule = collections.namedtuple(
    "ComparisonRule", ["target", "op", "value", "destination"]
)

type Workflow = list[Union[SimpleRule, ComparisonRule]]


class Day19(AOC.LineGroupAOC):
    DAY = 19

    def get_parts_ratings(self) -> List[PartRatings]:
        parts_ratings = []
        for line in self.input[1]:
            match = re.match(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", line)
            parts_ratings.append(PartRatings(*map(int, match.groups())))

        return parts_ratings

    def get_workflows(self) -> Dict[str, Workflow]:
        workflows = dict([self.parse_workflow(workflow) for workflow in self.input[0]])
        return workflows

    @staticmethod
    def parse_workflow(workflow: str) -> Workflow:
        name, rules = re.match(r"(\w+){(.+)}", workflow).groups()

        rules_parsed = []
        for rule in rules.split(","):
            split = re.split(r":|([<>])", rule)
            if len(split) == 5:
                target, op, value, _, destination = split
                if op == ">":
                    op = operator.gt
                else:
                    op = operator.lt

                rules_parsed.append(ComparisonRule(target, op, int(value), destination))
            else:
                rules_parsed.append(SimpleRule(*split))

        return name, rules_parsed

    @staticmethod
    def process_workflow(workflow: Workflow, part_ratings: PartRatings) -> str:
        for rule in workflow:
            match rule:
                case ComparisonRule():
                    if rule.op(getattr(part_ratings, rule.target), rule.value):
                        return rule.destination
                case SimpleRule():
                    return rule.destination

    @staticmethod
    def process_workflow_on_range(workflow: Workflow, part_ratings: RangeRatings):
        for rule in workflow:
            match rule:
                case SimpleRule():
                    return [(part_ratings, rule.destination)]

                case ComparisonRule():
                    _range: Range = getattr(part_ratings, rule.target)

                    if rule.op(_range, rule.value):
                        return [(part_ratings, rule.destination)]
                    elif rule.value in _range:
                        if rule.op is operator.lt:
                            if _range.start == rule.value:
                                continue

                            return [
                                (
                                    part_ratings._replace(
                                        **{
                                            rule.target: Range(
                                                _range.start, rule.value - 1
                                            )
                                        }
                                    ),
                                    rule.destination,
                                )
                            ] + Day19.process_workflow_on_range(
                                workflow,
                                part_ratings._replace(
                                    **{rule.target: Range(rule.value, _range.stop)}
                                ),
                            )

                        elif rule.op is operator.gt:
                            if _range.stop == rule.value:
                                continue

                            return [
                                (
                                    part_ratings._replace(
                                        **{
                                            rule.target: Range(
                                                rule.value + 1, _range.stop
                                            )
                                        }
                                    ),
                                    rule.destination,
                                )
                            ] + Day19.process_workflow_on_range(
                                workflow,
                                part_ratings._replace(
                                    **{rule.target: Range(_range.start, rule.value)}
                                ),
                            )

                    else:
                        continue

    def part_1(self):
        workflows = self.get_workflows()

        parts_status = dict()
        part_queue = queue.Queue()
        for part_ratings in self.get_parts_ratings():
            part_queue.put((part_ratings, "in"))

        while not part_queue.empty():
            part_ratings, destination = part_queue.get()
            next_destination = self.process_workflow(
                workflows[destination], part_ratings
            )

            if next_destination in ("A", "R"):
                parts_status[part_ratings] = next_destination

            else:
                part_queue.put((part_ratings, next_destination))

        return sum(
            [
                sum(part_ratings)
                for part_ratings, status in parts_status.items()
                if status == "A"
            ]
        )

    def part_2(self):
        workflows = self.get_workflows()

        accepted_ranges: [RangeRatings] = []

        range_queue = queue.Queue()
        range_queue.put(
            (
                RangeRatings(
                    x=Range(1, 4000),
                    m=Range(1, 4000),
                    a=Range(1, 4000),
                    s=Range(1, 4000),
                ),
                "in",
            )
        )
        while not range_queue.empty():
            ratings_range, workflow = range_queue.get()
            workflow = workflows[workflow]

            ranges = self.process_workflow_on_range(workflow, ratings_range)
            for new_ratings_range, destination in ranges:
                if destination in ("A", "R"):
                    if destination == "A":
                        accepted_ranges.append(new_ratings_range)
                else:
                    range_queue.put((new_ratings_range, destination))

        acc = 0
        for accepted_range in accepted_ranges:
            acc += math.prod([len(_range) for _range in accepted_range])

        return acc


if __name__ == "__main__":
    day_19 = Day19()
    print(day_19.part_2())
