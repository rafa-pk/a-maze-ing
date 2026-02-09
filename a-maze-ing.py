import sys


def main() -> None:
    if not len(sys.argv) == 2:
        print("Error: No arguments provided.\nUsage: a-maze-ing <config.txt>")
        sys.exit()
        params = MazeGenerator.Parser
        maze = MazeGenerator.generate(params)

if __name__ == "__main__":
    main()
