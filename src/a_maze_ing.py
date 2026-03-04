import sys
from typing import Optional
from maze_parser import MazeParser
from mazegen.generator import MazeGenerator
from maze_display import MLXHandler


class AMazeIng: 
    def __init__(self, config_file: str) -> None:
        self.parameters = MazeParser.parser(config_file)
        self.generator = self.new_instance(self.parameters.algorithm,
                                           self.parameters.seed)
        # self.window = MLXHandler(self.parameters)
        self.create_maze()
        # self.window.event_manager(self)

    def new_instance(self, algo: Optional[str] = None,
                     seed: Optional[int] = None) -> MazeGenerator:
        """"""
        return MazeGenerator(self.parameters.width,
                             self.parameters.height,
                             self.parameters.entry,
                             self.parameters.exit,
                             algo,
                             seed)

    def create_maze(self, generator: Optional[MazeGenerator] = None) -> None:
        """"""
                                                #TODO: ELLER: fix perfect maze avec pattern 42, pas de boucles dans les nums
        if generator:
            self.generator = generator
        self.generator.generate_maze(perfect=self.parameters.perfect)#, visualizer=maze_animation())
        self.solver = self.generator.BFS(self.generator)
        self.generator.create_output_file(self.parameters.output_file)
        print(f"Shortest path: {self.solver.get_path_string()}")
        self.generator.print_grid(path=self.solver.path)
        for row in self.generator.grid:
            for cell in row:
                print(cell.set_id, end=" ")
            print("")
        self.generator.print_as_nodegraph()

    # def maze_animation(self) -> None:
    #    self.window.update_full_image(self, self.settings)
    #    self.window.write_to_window()


def main() -> None:
    """"""
    if not len(sys.argv) == 2:
        print("Error: No arguments provided.\nUsage: python3 a-maze-ing.py "
              "<config.txt>")
        sys.exit(1)
    AMazeIng(sys.argv[1])


if __name__ == "__main__":
    main()
