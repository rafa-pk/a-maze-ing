import os
import sys
from typing import Dict
from enum import Enum


class MazeParser:
    """docstring"""
    class AllKeys(Enum):
        """"""
        WIDTH = "WIDTH"
        HEIGHT = "HEIGHT"
        ENTRY = "ENTRY"
        EXIT = "EXIT"
        OUTPUT_FILE = "OUTPUT_FILE"
        PERFECT = "PERFECT"
        ALGORITHM = "ALGORITHM"
        SEED = "SEED"

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
            sys.exit(1)
        maze_params = dict()

        try:
            with open(config_file, "r") as file:
                for line in file:
                    line = line.split("#", 1)[0].strip()
                    if not line:
                        continue
                    if "=" not in line:
                        raise ValueError("format is incorrect")
                    key, value = line.split("=", 1)
                    key = key.strip()
                    if cls.AllKeys(key):
                        maze_params[key] = value.strip()
        except Exception as error:
            print(f"Parsing Error: '{config_file}': {error}")
            sys.exit(1)
        return cls(maze_params)

    def __init__(self, maze_params: Dict[str, str]) -> None:
        """"""
        self.parameters = maze_params
        self.algorithm = None
        self.seed = None

        # print(f"Passed in dictionary {self.parameters}")
        try:
            for key in self.MandatoryKeys:
                if self.parameters.get(key.value) is None:
                    raise KeyError(f"Error: configuration file: Mandatory "
                                   f"field {key.value} not found or missing")
        except KeyError as error:
            print(f"{error}")
            sys.exit(1)
        try:
            self.width = int(self.parameters.get("WIDTH"))
            self.height = int(self.parameters.get("HEIGHT"))
            if self.height < 3 and self.width < 3:
                print("Parsing error: Maze is too small (minimum size is 3x3)")
                sys.exit(1)
        except ValueError as error:
            print(f"Parsing error: {error}\n\t       "
                  f"HEIGHT and WIDTH  must be valid integer values")
            sys.exit(1)
        try:
            x, y = self.parameters.get("ENTRY").split(",")
            self.entry = (int(x.strip()), int(y.strip()))
            if not (0 <= self.entry[0] < self.width and
                    0 <= self.entry[1] < self.height):
                print(f"Parsing error: Entry {self.entry} out of bounds")
                sys.exit(1)
        except (ValueError, IndexError) as error:
            print(f"Parsing error: {error}\n\t       "
                  f"ENTRY format must be 'ENTRY=x,y', where x and y are "
                  f"in-bounds integers")
            sys.exit(1)
        try:
            x, y = self.parameters.get("EXIT").split(",")
            self.exit = (int(x.strip()), int(y.strip()))
            if not (0 <= self.exit[0] < self.width and
                    0 <= self.exit[1] < self.height):
                print(f"Parsing error: Exit {self.exit} out of bounds")
                sys.exit(1)
        except (ValueError, IndexError) as error:
            print(f"Parsing error: {error}\n\t       "
                  f"EXIT format must be 'ENTRY=x,y', where x and y are "
                  f"in-bounds integers")
            sys.exit(1)
        if self.entry == self.exit:
            print("Parsing error: ENTRY and EXIT coordinates "
                  "must be different")
            sys.exit(1)
        self.output_file = self.parameters.get("OUTPUT_FILE").strip()
        if not self.output_file or not self.output_file.endswith(".txt"):
            print("Parsing error: output file must exist and end with .txt")
            sys.exit(1)
        self.perfect = self.parameters.get("PERFECT").strip()
        if self.perfect == "True":
            self.perfect = True
        elif self.perfect == "False":
            self.perfect = False
        else:
            print("Parsing error: PERFECT field must be of bool value "
                  "(True/False)")
            sys.exit(1)
        algo_str = self.parameters.get("ALGORITHM")
        if algo_str is not None:
            self.algorithm = algo_str.strip()
            if self.algorithm not in ["DFS", "Eller"]:
                print(f"Parsing error: '{self.algorithm}' not supported")
                sys.exit(1)
        seed_str = self.parameters.get("SEED")
        if seed_str is not None:
            try:
                self.seed = int(seed_str.strip())
                if self.seed < 0:
                    print("Parsing error: Seed cannot be negative")
                    sys.exit(1)
            except ValueError as error:
                print(f"Parsing error: SEED: {error}")
                sys.exit(1)
        # print(f"Attributes: width: {self.width} height: {self.height} entry
        # point: {self.entry} exit point: {self.exit} output file:
        # {self.output_file} perfect: {self.perfect}")


# if __name__ == "__main__":
#    MazeParser.parser(sys.argv[1])
