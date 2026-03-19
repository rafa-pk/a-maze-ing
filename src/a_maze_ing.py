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
        self.window = MLXHandler(self.parameters)
        self.color_ix = 1
        self.create_maze()
        self.window.event_manager(self)
        
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
        if generator:
            self.generator = generator
        self.generator.generate_maze(perfect=self.parameters.perfect)#, visualizer=maze_animation())
        self.solver = self.generator.BFS(self.generator)
        self.generator.create_output_file(self.parameters.output_file)
        print(f"Shortest path: {self.solver.get_path_string()}")
        for row in self.generator.grid:
            for cell in row:
                print(cell.set_id, end=" ")
            print("")
        self.generator.print_as_nodegraph()

    def maze_view(self, args: any) -> None:
        ptr, window, image, path = args
        self.path_flag = path
        if self.path_flag:
            self.grid_to_image(self.color_ix, path=self.solver.path)
        else:
            self.grid_to_image(self.color_ix, path=None)
        self.window.write_to_window(ptr, window, image)
        self.window.mlx.putstr(ptr, window, self.window.window_width // 5, 
                                self.window.window_height + self.window.cell_size, 0XFFFFFF, 
                               "ESC: quit; 1: path; 2: regen; 3: color; 4: algo")

    def key_handler(self, keycode: int, program: "AMazeIng") -> None:
        if keycode == 65307: #ESC: quit
            self.window.mlx.exit(self.window.ptr)
        elif keycode == 49: #1: path/no_path
            if self.path_flag:
                self.maze_view((self.window.ptr, self.window.window, self.window.image, False))
            else:
                self.maze_view((self.window.ptr, self.window.window, self.window.image, True))
        elif keycode == 50: #2: regen
            self.create_maze(self.new_instance(self.parameters.algorithm))
            self.maze_view((self.window.ptr, self.window.window, self.window.image, False))
        elif keycode == 51: #3: change colors
            if self.color_ix + 1 > len(self.window.color_scheme):
                self.color_ix = 1
            else:
                self.color_ix += 1
            self.maze_view((self.window.ptr, self.window.window, self.window.image, False))
        elif keycode == 52: #4: regen with other algo
            if self.parameters.algorithm is None or self.parameters.algorithm == "DFS":
                self.create_maze(self.new_instance("Eller"))
                self.parameters.algorithm = "Eller"
            elif self.parameters.algorithm == "Eller":
                self.create_maze(self.new_instance("DFS"))
                self.parameters.algorithm = "DFS"
            self.maze_view((self.window.ptr, self.window.window, self.window.image, False))
            
    def grid_to_image(self, ix: int, path: list = None) -> None:
        CELL_SIZE = self.window.cell_size
        BORDER_WIDTH = 2
        BORDER_COLOR = self.window.color_scheme[ix]["border"]
        LOGO_COLOR = self.window.color_scheme[ix]["logo"]
        PATH_COLOR = self.window.color_scheme[ix]["path"]
        BG_COLOR = self.window.color_scheme[ix]["bg"]

        path_cells: set = set()
        if path:
            cx, cy = self.generator.entry_point
            path_cells.add((cx, cy))
            for direction in path:
                dx, dy = self.generator.Directions[direction]
                cx += dx
                cy += dy
                path_cells.add((cx, cy))

        for y in range(self.generator.height):
            for x in range(self.generator.width):
                cell = self.generator.grid[y][x]
                px = x * CELL_SIZE
                py = y * CELL_SIZE
                if (x, y) in path_cells:
                    color = PATH_COLOR
                    self.window.draw_rect(color, px, py, CELL_SIZE - 2, CELL_SIZE - 2)
                else:
                    color = BG_COLOR
                    self.window.draw_rect(color, px, py, CELL_SIZE, CELL_SIZE)
                if cell.north:
                    self.window.draw_rect(BORDER_COLOR, px, py, CELL_SIZE, BORDER_WIDTH)
                if cell.south:
                    self.window.draw_rect(BORDER_COLOR, px, py + CELL_SIZE, CELL_SIZE, BORDER_WIDTH)
                if cell.east:
                    self.window.draw_rect(BORDER_COLOR, px + CELL_SIZE - BORDER_WIDTH, py, BORDER_WIDTH, CELL_SIZE)
                if cell.west:
                    self.window.draw_rect(BORDER_COLOR, px, py, BORDER_WIDTH, CELL_SIZE)
                if (x, y) in self.generator.pattern_cells:
                    self.window.draw_rect(LOGO_COLOR, px, py, CELL_SIZE, CELL_SIZE)
                if (x, y) == self.generator.entry_point:
                    self.window.draw_rect(0X00FF00, px, py, CELL_SIZE, CELL_SIZE)
                if (x, y) == self.generator.exit_point:
                    self.window.draw_rect(0X0096FF, px, py, CELL_SIZE, CELL_SIZE)
    
def main() -> None:
    """"""
    if not len(sys.argv) == 2:
        print("Error: No arguments provided.\nUsage: python3 a-maze-ing.py "
              "<config.txt>")
        sys.exit(1)
    AMazeIng(sys.argv[1])


if __name__ == "__main__":
    main()
