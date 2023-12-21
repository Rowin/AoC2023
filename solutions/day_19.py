from operator import lt, gt

from utils import AOC


class Day19(AOC.LineGroupAOC):
    DAY = 19

    @staticmethod
    def get_rules(rules):
        rules_command = []
        for rule in rules:
            match rule.split(":"):
                case condition, destination:
                    if "<" in condition:
                        sep = "<"
                    else:
                        sep = ">"

                    label, target = condition.split(sep)

                    rules_command.append(
                        f"if part.{label} {sep} {target}: return {destination}"
                    )

                case destination:
                    rules_command.append(f"return {destination}")

        def rules(part):
            for rule in rules_command:
                exec(rule)

        return rules

    @staticmethod
    def exec_workflow(part_rating, workflow):
        for rule in workflow:
            match rule.split(":"):
                case condition, destination:
                    if "<" in condition:
                        sep = lt
                    else:
                        sep = gt

                    label, target = condition.split(sep)
                    if sep(part_rating[label], int(target)):
                        return destination

                case destination:
                    return destination

    def part_1(self):
        workflows = self.input[0]
        parts_ratings = self.input[1]

        parts_ratings = []
        for part_ratings in self.input[1]:
            (ratings,) = part_ratings[1:-1].split(",")
            parts_ratings.append(
                {category: int(score) for category, score in ratings.split("=")}
            )

        workflows_dict = dict()
        for workflow in workflows:
            name, rules = workflow.split("{")
            rules = rules[:-1].split(",")
            workflows_dict[name] = rules

        parts_destination = []
        for part_ratings in parts_ratings:
            current_workflow = "in"
            while True:
                destination = self.exec_workflow(
                    part_ratings, workflows_dict[current_workflow]
                )
                if destination in ("A", "R"):
                    break

                current_workflow = destination

            parts_destination.append(destination)

        print(parts_destination)

    def part_2(self):
        pass


if __name__ == "__main__":
    day_19 = Day19()
    print(day_19.part_1())
