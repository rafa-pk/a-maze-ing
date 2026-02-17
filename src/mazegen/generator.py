import sys
import random
from dataclasses import dataclass
from typing import Optional
from maze_parser import MazeParser


class MazeGenerator:
    """exportable module to mazegenerator package"""
    Directions: dict[str, tuple[int, int]] = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }

    Opposite: dict[str, str] = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E",
    }

    Digit_4: list[tuple[int, int]] = [
        (0, 0), (0, 1), (0, 2),
        (1, 2),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
    ]

    Digit_2: list[tuple[int, int]] = [
        (0, 0), (1, 0), (2, 0),
        (2, 1),
        (0, 2), (1, 2), (2, 2),
        (0, 3),
        (0, 4), (1, 4), (2, 4),
    ]

    @dataclass
    class Cell:
        x: int
        y: int
        val: int = 0
        north: bool = True
        east: bool = True
        south: bool = True
        west: bool = True
        visited: bool = False

    def __init__(self, parameters: MazeParser) -> None:
        """"""
        self.width: int = parameters.width
        self.height: int = parameters.height
        self.entry: tuple[int, int] = parameters.entry
        self.exit: tuple[int, int] = parameters.exit
        self.seed: Optional[int] = parameters.seed

        self.grid: list[list[self.Cell]] = [
            [self.Cell(x=width, y=height) for width in range(self.width)]
             for height in range(self.height)
        ]
        
        if parameters.seed is not None:
            self.seed: int = parameters.seed
        else:
            self.seed = random.randint(0, 2**32 - 1)

        def get_cell(self, x: int, y: int) -> self.Cell:
            return self.grid[y][x]

        def place_pattern_42(self, x: int, y: int) -> self.Cell:
            if self.width < Pattern_width or self.height < Pattern_height:
                print("Warning: maze too small for 42 pattern, skipping")
                return

            offset_x: int = (self.width - Pattern_width) // 2
            offset_y: int = (self.height - Pattern_height) // 2
            for px, py in Digit_4:
                self.pattern_cells.add((offset_x + px, offset_y + py))
            for px, py in Digit_2:
                self.pattern_cells.add((offset_x + 5 + px, offset_y + py))

            if self.entry in self.pattern_cells:
                print("Warning: entry overlaps 42 pattern, skipping pattern")
                self.pattern_cells.clear()
                return
            if self.exit in self.pattern_cells:
                print("Warning: exit overlaps 42 pattern, skipping pattern")
                self.pattern_cells.clear()
                return
            for px, py, in self.pattern_cells:
                self.grid[py][px].visited = True
                self.val = 1
            self.place_pattern_42()

    def print_grid(self):
        """"""
        for row in self.grid:
            for cell in row:
                print(cell.val, end="")
            print()
