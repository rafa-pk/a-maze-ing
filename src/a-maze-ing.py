import sys


class AMazeIng:
    """main program orchestrator class"""
    def __init__(self, config_file: str):
        config = MazeParser.parser(config_file)

def main() -> None:
    if not len(sys.argv) == 2:
        print("Error: No arguments provided.\nUsage: python3 a-maze-ing "
              "<config.txt>")
        sys.exit()
    AMazeIng(sys.argv[1])


if __name__ == "__main__":
    main()
