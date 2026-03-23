import sys
from typing import Optional, Any
from maze_parser import MazeParser
from mazegen.generator import MazeGenerator
from maze_display import MLXHandler


# =============================================================================
# MAIN APPLICATION
# =============================================================================
class AMazeIng:
    """Orchestrate maze generation, solving, rendering and user interaction.

    Ties together MazeParser, MazeGenerator, and MLXHandler to parse
    the config, generate and solve the maze, display it in a window
    and handle keyboard events.
    """
    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------
    def __init__(self, config_file: str) -> None:
        """Parse config, generate the maze and open the display window."""
        self.parameters = MazeParser.parser(config_file)
        self.generator = self.new_instance(self.parameters.algorithm,
                                           self.parameters.seed)
        self.window = MLXHandler(self.parameters)
        self.color_ix = 1
        self.create_maze()
        self.path_flag: bool = False
        self.solution_steps: list[tuple[int, int]] = []
        self.window.event_manager(self)

    def new_instance(self, algo: Optional[str] = None,
                     seed: Optional[int] = None) -> MazeGenerator:
        """Create and return a fresh MazeGenerator from current parameters"""
        return MazeGenerator(self.parameters.width,
                             self.parameters.height,
                             self.parameters.entry,
                             self.parameters.exit,
                             algo,
                             seed)

    # -------------------------------------------------------------------------
    # Maze Generation & Solving
    # -------------------------------------------------------------------------
    def create_maze(self, generator: Optional[MazeGenerator] = None) -> None:
        """Generate the maze, solve it and write the output file.

        Replaces the current generator if one is provided, then runs
        generation, BFS solving, file export and solution step building.
        """
        if generator:
            self.generator = generator
        self.window.solving = False
        self.window.step_index = 0
        self.window.frame_counter = 0
        self.solution_steps = []

        self.generator.generate_maze(perfect=self.parameters.perfect)
        self.solver = self.generator.BFS(self.generator)
        self.generator.create_output_file(self.parameters.output_file)
        self._build_solution_steps()
        print(f"Shortest path: {self.solver.get_path_string()}")

    def maze_view(self, args: tuple[Any, Any, Any, bool]) -> None:
        """Render the maze grid to the image buffer and push to the window.

        Draws the maze with or without the solution path depending on
        the path flag, then overlays the keybinding hint string.
        """
        ptr, window, image, path = args
        self.path_flag = path
        if self.path_flag:
            self.grid_to_image(self.color_ix, path=self.solver.path)
        else:
            self.grid_to_image(self.color_ix, path=None)
        self.window.write_to_window(ptr, window, image)
        self.window.mlx.putstr(ptr, window, self.window.window_width // 5,
                               self.window.window_height +
                               self.window.cell_size, 0XFFFFFF,
                               "ESC: quit; 1: path; 2: regen; 3: color;"
                               "4: algo; 5: anim")

    def key_handler(self, keycode: int, program: "AMazeIng") -> None:
        """Handle keyboard input to control the maze display.

        Keybindings:
            ESC (65307): Quit the program.
            1   (49):    Toggle solution path display.
            2   (50):    Regenerate the maze with the current algorithm.
            3   (51):    Cycle through color schemes.
            4   (52):    Regenerate with the alternate algorithm.
            5   (53):    Toggle step-by-step solution animation.
        """
        if keycode == 65307:
            self.window.mlx.exit(self.window.ptr)
        elif keycode == 49:
            self.window.solving = False
            if self.path_flag:
                self.maze_view((self.window.ptr, self.window.window,
                                self.window.image, False))
                self.path_flag = False
            else:
                self.maze_view((self.window.ptr, self.window.window,
                                self.window.image, True))
                self.path_flag = True
        elif keycode == 50:
            self.create_maze(self.new_instance(self.parameters.algorithm,
                                               self.parameters.seed))
            self.maze_view((self.window.ptr, self.window.window,
                            self.window.image, False))
        elif keycode == 51:
            if self.color_ix + 1 > len(self.window.color_scheme):
                self.color_ix = 1
            else:
                self.color_ix += 1
            was_animating = self.window.solving
            self.window.solving = False
            self.maze_view((self.window.ptr, self.window.window,
                            self.window.image, False))
            if was_animating:
                self.window.start_solve_animation(
                    self.solution_steps,
                    scheme=self.color_ix,
                    frame_delay=1,
                    steps_per_frame=5,
                )
        elif keycode == 52:
            if (self.parameters.algorithm is None
                    or self.parameters.algorithm == "DFS"):
                self.create_maze(self.new_instance("Eller"))
                self.parameters.algorithm = "Eller"
            elif self.parameters.algorithm == "Eller":
                self.create_maze(self.new_instance("DFS"))
                self.parameters.algorithm = "DFS"
            self.maze_view((self.window.ptr, self.window.window,
                            self.window.image, False))
        elif keycode == 53:
            if self.window.solving:
                self.window.solving = False
                self.maze_view((self.window.ptr, self.window.window,
                                self.window.image, False))
                self.path_flag = False
            else:
                self.maze_view((self.window.ptr, self.window.window,
                                self.window.image, False))
                self.window.start_solve_animation(
                    self.solution_steps,
                    scheme=self.color_ix,
                    frame_delay=1,
                    steps_per_frame=5
                )
                self.path_flag = True

    def grid_to_image(self, ix: int, path: Optional[list[Any]] = None) -> None:
        """Draw the full maze grid into the image buffer.

        Renders cell backgrounds, walls, path overlay, 42 pattern cells,
        and entry/exit highlights using the selected color scheme.
        """
        CELL_SIZE = self.window.cell_size
        BORDER_WIDTH = 2
        BORDER_COLOR = self.window.color_scheme[ix]["border"]
        LOGO_COLOR = self.window.color_scheme[ix]["logo"]
        PATH_COLOR = self.window.color_scheme[ix]["path"]
        BG_COLOR = self.window.color_scheme[ix]["bg"]

        path_cells: set[tuple[int, int]] = set()
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
                    self.window.draw_rect(color, px, py, CELL_SIZE - 2,
                                          CELL_SIZE - 2)
                else:
                    color = BG_COLOR
                    self.window.draw_rect(color, px, py, CELL_SIZE, CELL_SIZE)
                if cell.north:
                    self.window.draw_rect(BORDER_COLOR, px, py, CELL_SIZE,
                                          BORDER_WIDTH)
                if cell.south:
                    self.window.draw_rect(BORDER_COLOR, px, py + CELL_SIZE,
                                          CELL_SIZE, BORDER_WIDTH)
                if cell.east:
                    self.window.draw_rect(BORDER_COLOR, px + CELL_SIZE -
                                          BORDER_WIDTH, py, BORDER_WIDTH,
                                          CELL_SIZE)
                if cell.west:
                    self.window.draw_rect(BORDER_COLOR, px, py, BORDER_WIDTH,
                                          CELL_SIZE)
                if (x, y) in self.generator.pattern_cells:
                    self.window.draw_rect(LOGO_COLOR, px, py, CELL_SIZE,
                                          CELL_SIZE)
                if (x, y) == self.generator.entry_point:
                    self.window.draw_rect(0X00FF00, px, py, CELL_SIZE,
                                          CELL_SIZE)
                if (x, y) == self.generator.exit_point:
                    self.window.draw_rect(0X0096FF, px, py, CELL_SIZE,
                                          CELL_SIZE)

    def _build_solution_steps(self) -> None:
        """Convert the BFS path directions into ordered (x, y) coordinates.

        Walks from the entry point following each direction in the path
        and stores each visited cell for the animation renderer.
        """
        steps = []
        cx, cy = self.generator.entry_point
        steps.append((cx, cy))
        for direction in self.solver.path:
            dx, dy = self.generator.Directions[direction]
            cx += dx
            cy += dy
            steps.append((cx, cy))
        self.solution_steps = steps


def main() -> None:
    """Validate arguments and launch the maze application.

    Expects exactly one argument: the path to the config file.
    """
    if not len(sys.argv) == 2:
        print("Error: No arguments provided.\nUsage: python3 a-maze-ing.py "
              "<config.txt>")
        sys.exit(1)
    AMazeIng(sys.argv[1])


if __name__ == "__main__":
    main()
