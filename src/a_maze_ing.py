import sys
from maze_parser import MazeParser
from mazegen.generator import MazeGenerator

class AMazeIng:
    """main program orchestrator class"""
    def __init__(self, config_file: str) -> None:
        self.parameters = MazeParser.parser(config_file)
        self.maze = MazeGenerator(self.parameters)
        self.width = self.parameters.width
        self.height = self.parameters.height
        self.maze.print_grid()


def main() -> None:
    if not len(sys.argv) == 2:
        print("Error: No arguments provided.\nUsage: python3 a-maze-ing "
              "<config.txt>")
        sys.exit()
    AMazeIng(sys.argv[1])


if __name__ == "__main__":
    main()
