import sys
from dataclasses import dataclass
from typing import Optional
from maze_parser import MazeParser


class MazeGenerator:
    """exportable module to mazegenerator package"""
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

    #def print_grid(self):
    #    """"""
    #    for row in self.grid:
    #        for cell in row:
    #            print(cell.val, end="")
    #        print()
