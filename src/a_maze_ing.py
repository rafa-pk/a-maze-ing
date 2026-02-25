import sys
from maze_parser import MazeParser
from mazegen.generator import MazeGenerator


class AMazeIng:

    def __init__(self, config_file: str) -> None:
        self.parameters = MazeParser.parser(config_file)
        self.generator = self.new_instance(self.parameters.algorithm,
                                      self.parameters.seed)
        self.solver = self.generator.BFS(self.generator)
        #self.window = 

        self.create_maze()

    def new_instance(self, algo: str | None = None, 
                 seed: int | None = None) -> MazeGenerator:
        """"""
        return MazeGenerator(self.parameters.width, 
                self.parameters.height, 
                self.parameters.entry, 
                self.parameters.exit,
                algo,
                seed)

    def create_maze(self, generator: MazeGenerator | None = None) -> None:
        """"""
        
        if generator:
            self.generator = generator
        self.generator.generate_maze(perfect=self.parameters.perfect) 
                                     #visualizer=self.maze_animation)
        self.generator.BFS(self.generator)
        #self.generator.create_output_file(self.parameters.output_file)
        #print(f"Shortest path: {self.solver.get_path_string()}")
        self.generator.print_grid(path=self.solver.path)


   #def maze_animation(self) -> None:
       

def main() -> None:
    """"""
    if not len(sys.argv) == 2:
        print("Error: No arguments provided.\nUsage: python3 a-maze-ing.py "
              "<config.txt>")
        sys.exit(1)
    AMazeIng(sys.argv[1]) 

if __name__ == "__main__":
    main()
