from abc import abstractmethod, ABC
from pathlib import Path
import requests


class BaseAOC(ABC):
    YEAR = '2022'

    def __init__(self, day):
        self.day = day
        self.retrieve_input()
        self.parse_input()

    def retrieve_input(self) -> None:
        path = Path(f'./inputs/day_{self.day}.txt')
        if not path.is_file():
            self.raw_input = self.download_input()
            with open(path, "w") as file_input:
                file_input.write(self.raw_input)

        else:
            with open(path, "r") as file_input:
                self.raw_input = file_input.read()

    def download_input(self) -> str:
        cookies = {'session': '53616c7465645f5f7344bcfd0d0927d073862b8676877ba3d9d7e13795274462656a12581213b0a79fbe84b4a865715cc717be388f98ece1cf7c93c84a3b657f'}

        r = requests.get(f"https://adventofcode.com/{self.YEAR}/day/{self.day}/input", cookies=cookies, verify=False)

        if r.status_code == 200:
            return r.text
        else:
            raise ConnectionError

    @abstractmethod
    def parse_input(self):
        ...


class LinearAOC(BaseAOC):
    def parse_input(self):
        self.input = self.raw_input.split('\n')