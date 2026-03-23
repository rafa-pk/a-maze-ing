import os
import sys
from typing import Dict
from enum import Enum


# =============================================================================
# MAZE CONFIGURATION KEYS
# =============================================================================
class MazeParser:
    """Parse and validate the maze configuration file.

    Ensures all mandatory keys are present and that no unknown
    keys are included in the configuration.
    """
    class AllKeys(Enum):
        """All valid keys accepted in the configuration file."""
        WIDTH = "WIDTH"
        HEIGHT = "HEIGHT"
        ENTRY = "ENTRY"
        EXIT = "EXIT"
        OUTPUT_FILE = "OUTPUT_FILE"
        PERFECT = "PERFECT"
        ALGORITHM = "ALGORITHM"
        SEED = "SEED"

    class MandatoryKeys(Enum):
        """ ALGORITHM and SEED are optional and therefore excluded."""
        WIDTH = "WIDTH"
        HEIGHT = "HEIGHT"
        ENTRY = "ENTRY"
        EXIT = "EXIT"
        OUTPUT_FILE = "OUTPUT_FILE"
        PERFECT = "PERFECT"

    # -------------------------------------------------------------------------
    # Config File Parsing
    # -------------------------------------------------------------------------
    @classmethod
    def parser(cls, config_file: str) -> "MazeParser":
        """Read and parse a config file into key-value maze parameters.

        Skips blank lines and inline comments. Expects each valid
        line to follow the format: KEY = VALUE.
        """
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

    # -------------------------------------------------------------------------
    # Initialization & Validation
    # -------------------------------------------------------------------------
    def __init__(self, maze_params: Dict[str, str]) -> None:
        """Initialize and validate all maze parameters from the config file.

        Validates mandatory keys, dimensions, entry/exit coordinates,
        output file, maze type, and optional algorithm and seed.
        """
        self.parameters = maze_params
        self.algorithm = None
        self.seed = None

        # -- Mandatory keys check --
        try:
            for key in self.MandatoryKeys:
                if self.parameters.get(key.value) is None:
                    raise KeyError(f"Error: configuration file: Mandatory "
                                   f"field {key.value} not found or missing")
        except KeyError as error:
            print(f"{error}")
            sys.exit(1)
        # -- Dimensions --
        try:
            self.width = int(self.parameters.get("WIDTH") or 0)
            self.height = int(self.parameters.get("HEIGHT") or 0)
            if self.height < 3 and self.width < 3:
                print("Parsing error: Maze is too small (minimum size is 3x3)")
                sys.exit(1)
        except ValueError as error:
            print(f"Parsing error: {error}\n\t       "
                  f"HEIGHT and WIDTH  must be valid integer values")
            sys.exit(1)

        # -- Entry coordinates --
        try:
            x, y = (self.parameters.get("ENTRY") or "").split(",")
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

        # -- Exit coordinates --
        try:
            x, y = (self.parameters.get("EXIT") or "").split(",")
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

        # -- Output file --
        self.output_file = (self.parameters.get("OUTPUT_FILE") or "").strip()
        if not self.output_file or not self.output_file.endswith(".txt"):
            print("Parsing error: output file must exist and end with .txt")
            sys.exit(1)

        # -- Perfect maze flag --
        self.perfect: bool = False
        perfect_str = (self.parameters.get("PERFECT") or "").strip()
        if perfect_str == "True":
            self.perfect = True
        elif perfect_str == "False":
            self.perfect = False
        else:
            print("Parsing error: PERFECT field must be of bool value "
                  "(True/False)")
            sys.exit(1)

        # -- Optional: algorithm --
        try:
            algo_str = self.parameters.get("ALGORITHM")
            if algo_str is not None:
                self.algorithm = algo_str.strip()
            if self.algorithm not in ["DFS", "Eller", None]:
                raise ValueError(f"'{self.algorithm}' not supported, "
                                 f"choose 'DFS' or 'Eller'")
        except ValueError as error:
            print(f"Parsing error: ALGORITHM: {error}")
            sys.exit(1)

        # -- Optional: seed --
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
