import itertools
from collections import namedtuple

from utils import AOC


class Day24(AOC.LinearAOC):
    DAY = 24

    def part_1(self):
        BOUNDARIES_MIN = 200_000_000_000_000
        BOUNDARIES_MAX = 400_000_000_000_000

        Trajectory = namedtuple("Trajectory", ["a", "b", "init_pos", "init_vel"])
        Vector = namedtuple("Vector", ["x", "y", "z"])
        trajectories: [Trajectory] = []
        for line in self.input:
            position, velocity = line.split(" @ ")
            x, y, z = map(int, position.split(", "))
            vx, vy, vz = map(int, velocity.split(", "))

            a = vy / vx
            b = y - a * x

            trajectories.append(Trajectory(a, b, Vector(x, y, z), Vector(vx, vy, vz)))

        valid_collisions_count = 0
        for traj1, traj2 in itertools.combinations(trajectories, r=2):
            try:
                xi = (traj2.b - traj1.b) / (traj1.a - traj2.a)
                yi = (traj1.a * traj2.b - traj1.b * traj2.a) / (traj1.a - traj2.a)

                if (
                    BOUNDARIES_MIN <= xi <= BOUNDARIES_MAX
                    and BOUNDARIES_MIN <= yi <= BOUNDARIES_MAX
                ):
                    t1 = (xi - traj1.init_pos.x) / traj1.init_vel.x
                    t2 = (xi - traj2.init_pos.x) / traj2.init_vel.x
                    if t1 >= 0 and t2 >= 0:
                        valid_collisions_count += 1

            except ZeroDivisionError:
                ...

        return valid_collisions_count

    def part_2(self):
        pass


if __name__ == "__main__":
    day_24 = Day24()
    print(day_24.part_1())
