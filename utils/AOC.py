from abc import abstractmethod, ABC
from pathlib import Path
from typing import Any
from importlib import resources

import numpy as np
import requests
import numpy.typing as npt

from .config import config
import inputs


class BaseAOC(ABC):
    YEAR = config.year
    DAY: int

    def __init__(self):
        self.day = self.DAY
        self.retrieve_input()
        self.parse_input()
        self.raw_input: str
        self.input: Any

    @abstractmethod
    def part_1(self):
        ...

    @abstractmethod
    def part_2(self):
        ...

    def retrieve_input(self) -> None:
        path = resources.files(inputs) / f"day_{self.day}.txt"
        if not path.is_file():
            self.raw_input = self.download_input()
            with path.open("w") as file_input:
                file_input.write(self.raw_input)

        else:
            with path.open("r") as file_input:
                self.raw_input = file_input.read()

    def download_input(self) -> str:
        cookies = {"session": config.session_id}

        r = requests.get(
            f"https://adventofcode.com/{self.YEAR}/day/{self.day}/input",
            cookies=cookies,
            verify=False,
        )

        if r.status_code == 200:
            return r.text
        else:
            raise ConnectionError(r.text)

    @abstractmethod
    def parse_input(self):
        ...


class LinearAOC(BaseAOC, ABC):
    def parse_input(self):
        self.input = self.raw_input.splitlines()


class GridAOC(BaseAOC, ABC):
    def parse_input(self):
        self.input: npt.NDArray = np.array(
            [list(line) for line in self.raw_input.splitlines()]
        )


class LineGroupAOC(BaseAOC, ABC):
    def parse_input(self):
        tmp_input = self.raw_input.splitlines()

        self.input = []
        acc = []
        for line in tmp_input:
            if line == "":
                self.input.append(acc)
                acc = []
                continue
            acc.append(line)
        else:
            self.input.append(acc)


class GridGroupAOC(LineGroupAOC, ABC):
    def parse_input(self):
        super().parse_input()
        grid_input = []
        for group in self.input:
            grid_input.append(np.array([list(line) for line in group]))

        self.input = grid_input
