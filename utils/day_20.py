import dataclasses
import enum
import queue
from abc import abstractmethod
from collections import defaultdict
from typing import Optional, List, Self

from tqdm import tqdm

from utils import AOC


class Pulse(enum.IntEnum):
    HIGH = 1
    LOW = 0


class State(enum.Flag):
    ON = 1
    OFF = 0


@dataclasses.dataclass
class Event:
    pulse: Pulse
    destination: str
    inp: str

    def __repr__(self):
        return f"{self.inp} -{self.pulse}-> {self.destination}"


class BaseModule:
    def __init__(self, destinations: Optional[List] = None):
        if destinations is None:
            destinations = []
        self.destinations = destinations
        self.inputs = []

    def register_input(self, inp):
        self.inputs.append(inp)

    def receive_pulse(self, pulse: Pulse, inp) -> tuple[Optional[Pulse], [str]]:
        return self.send_pulse()

    def send_pulse(
        self, pulse: Optional[Pulse] = None
    ) -> tuple[Optional[Pulse], [str]]:
        return pulse, self.destinations


class FlipFlopModule(BaseModule):
    def __init__(self, *args):
        super().__init__(*args)
        self.state = State.OFF

    def receive_pulse(self, pulse: Pulse, inp) -> tuple[Optional[Pulse], [str]]:
        if pulse is Pulse.HIGH:
            return None, []
        elif pulse is Pulse.LOW:
            self.state = ~self.state

            if self.state is State.ON:
                return self.send_pulse(Pulse.HIGH)
            elif self.state is State.OFF:
                return self.send_pulse(Pulse.LOW)


class ConjunctionModule(BaseModule):
    def __init__(self, *args):
        super().__init__(*args)
        self.inputs_state = dict()

    def register_input(self, inp):
        self.inputs_state[inp] = Pulse.LOW

    def receive_pulse(self, pulse: Pulse, inp) -> tuple[Optional[Pulse], [str]]:
        self.inputs_state[inp] = pulse

        if all(self.inputs_state.values()):
            return self.send_pulse(Pulse.LOW)
        else:
            return self.send_pulse(Pulse.HIGH)

    @classmethod
    def from_existing_module(cls, existing_module: BaseModule, destinations) -> Self:
        new_module = cls(destinations)
        for inp in existing_module.inputs:
            new_module.register_input(inp)

        return new_module


class BroadcastModule(BaseModule):
    def receive_pulse(self, pulse: Pulse, inp) -> tuple[Optional[Pulse], [str]]:
        return self.send_pulse(pulse)


class Day20(AOC.LinearAOC):
    DAY = 20

    def part_1(self):
        self.modules = self.get_modules_from_input()
        self.pulse_history = []

        pulse_queue = queue.Queue()

        for i in range(1_000_000):
            pulse_queue.put(Event(Pulse.LOW, "broadcaster", "button"))
            self.process_queue(pulse_queue)

        high_pulse_count = sum(self.pulse_history)
        low_pulse_count = len(self.pulse_history) - high_pulse_count
        return low_pulse_count * high_pulse_count

    def part_2(self):
        pass

    def process_queue(self, event_queue: queue.Queue[Event]):
        while not event_queue.empty():
            event = event_queue.get()
            self.pulse_history.append(event.pulse)

            module_name = event.destination
            module: BaseModule = self.modules[module_name]
            pulse, destinations = module.receive_pulse(event.pulse, event.inp)
            if module_name in ("lf", "br", "fk", "rz") and pulse is Pulse.HIGH:
                print(self.button_press, module_name, self.modules["lb"].inputs_state)
            for destination in destinations:
                event_queue.put(Event(pulse, destination, module_name))

    def get_modules_from_input(self):
        modules = defaultdict(BaseModule)

        for line in self.input:
            module_name, destinations = line.split(" -> ")

            destinations = destinations.split(", ")
            if module_name.startswith("%"):
                module_name = module_name[1:]
                modules[module_name] = FlipFlopModule(destinations)
            elif module_name.startswith("&"):
                module_name = module_name[1:]
                existing_module = modules[module_name]
                modules[module_name] = ConjunctionModule.from_existing_module(
                    existing_module, destinations
                )
            else:
                modules[module_name] = BroadcastModule(destinations)

            for destination in destinations:
                modules[destination].register_input(module_name)

        return modules

    @staticmethod
    def as_dot(modules: dict):
        for module_name, module in modules.items():
            if isinstance(module, FlipFlopModule):
                pref = "%"
                color = "red"
            elif isinstance(module, ConjunctionModule):
                pref = "&"
                color = "orange"
            else:
                pref = ""
                color = "blue"

            print(f'{module_name} [color={color},label="{pref}{module_name}"];')
            print(f"{module_name} ->  {{{' '.join(module.destinations)}}};")


if __name__ == "__main__":
    day_20 = Day20()
    # day_20.as_dot(day_20.get_modules_from_input())
    day_20.part_1()
