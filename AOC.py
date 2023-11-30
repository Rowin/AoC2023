from abc import abstractmethod, ABC
from pathlib import Path

import requests

from config import config


class BaseAOC(ABC):
    YEAR = config.year

    def __init__(self, day):
        self.day = day
        self.retrieve_input()
        self.parse_input()

    def retrieve_input(self) -> None:
        path = Path(f"./inputs/day_{self.day}.txt")
        if not path.is_file():
            self.raw_input = self.download_input()
            with open(path, "w") as file_input:
                file_input.write(self.raw_input)

        else:
            with open(path, "r") as file_input:
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


class LinearAOC(BaseAOC):
    def parse_input(self):
        self.input = self.raw_input.split("\n")