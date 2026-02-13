import os
import sys
from typing import Dict
from enum import Enum


class MazeParser:
    """docstring"""
    #class AllKeys(Enum):

    class MandatoryKeys(Enum):
        """"""
        WIDTH = "WIDTH"
        HEIGHT = "HEIGHT"
        ENTRY = "ENTRY"
        EXIT = "EXIT"
        OUTPUT_FILE = "OUTPUT_FILE"
        PERFECT = "PERFECT"

    @classmethod
    def parser(cls, config_file: str) -> "MazeParser":
        """"""
        if not os.path.isfile(config_file):
            print(f"Error: {config_file} not valid or not found")
            sys.exit()
        maze_params = dict()

        try:
            with open(config_file, "r") as file:
                for line in file:
                    line = line.split("#", 1)[0].strip()
                    if not line:
                        continue
                    if "=" not in line:
                        raise ValueError(f"Error: {config_file}:"
                                     f"format is incorrect")
                    key, value = line.split("=", 1)
                    key = key.strip()
                    if cls.MandatoryKeys(key):
                        maze_params[key] = value.strip()
        except Exception as error:
            print(f"Parsing Error: {config_file}: {error}"
                  f"or not found")
            sys.exit()
        return cls(maze_params)

    def __init__(self, maze_params: Dict[str, str]) -> None:
        """"""
        self.parameters = maze_params
        print(f"{self.parameters}")


if __name__ == "__main__":
    MazeParser.parser("../config.txt")
