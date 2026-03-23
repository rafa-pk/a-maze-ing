import random
from typing import Optional, Union
from random import randint
from dataclasses import dataclass
from collections import deque
from collections import defaultdict


class MazeGenerator:
    # -------------------------------------------------------------------------
    # Parameters Initializion
    # -------------------------------------------------------------------------
    """Generate mazes using configurable algorithms and parameters.

    Directions and Opposite are used during maze generation to navigate
    between cells and carve walls.
    Digit_4 and Digit_2 define 42 pixel patterns.
    Pattern_width, Pattern_height, Min_width and Min_height set the
    minimum maze dimensions required to render those patterns correctly.
    """
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
    Pattern_width: int = 7
    Pattern_height: int = 5
    Min_width: int = 9
    Min_height: int = 7

    # -------------------------------------------------------------------------
    # Grid Initializion
    # -------------------------------------------------------------------------
    @dataclass
    class Cell:
        """Represent a single maze cell and its wall state.

        All walls are open by default and get carved during generation.
        """
        x: int
        y: int
        north: bool = True
        east: bool = True
        south: bool = True
        west: bool = True
        visited: bool = False
        set_id: int = -1

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------
    def __init__(self, width: int, height: int,
                 entry_point: tuple[int, int], exit_point: tuple[int, int],
                 algo:
                 Optional[str] = None, seed: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self.entry_point = entry_point
        self.exit_point = exit_point
        self.pattern_cells: set[tuple[int, int]] = set()
        # Default algo when not specified.
        if algo is None:
            self.algo = "DFS"
        else:
            self.algo = algo
        # seed random configuration.
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        self.seed = seed
        random.seed(seed)
        self.grid: list[list["MazeGenerator.Cell"]] = [
            [self.Cell(x=x, y=y) for x in range(self.width)]
            for y in range(self.height)
        ]

    # -------------------------------------------------------------------------
    # Generate maze
    # -------------------------------------------------------------------------
    def generate_maze(self, perfect: bool = True) -> None:
        """Generate the maze grid using the configured algorithm.

        Places the 42 pattern before generation if DFS is used.
        """
        self.perfect = perfect
        if self.algo == "DFS":
            self._place_42_pattern()
            self.DFS(self)
        elif self.algo == "Eller":
            self.Eller(self)

    # -------------------------------------------------------------------------
    # Return cell
    # -------------------------------------------------------------------------
    def get_cell(self, x: int, y: int) -> "MazeGenerator.Cell":
        """Return a cell of the grid"""
        return self.grid[y][x]

    # -------------------------------------------------------------------------
    # Place 42 pattern
    # -------------------------------------------------------------------------
    def _place_42_pattern(self) -> None:
        """Place the '42' digit pattern at the center of the maze grid.

        Marks the pattern cells as visited so generation algorithms
        carve around them. Error message if the grid is too small or if
        entry/exit coordinates overlap the pattern.
        """
        if (self.width < self.Min_width
                or self.height < self.Min_height):
            print("Warning: maze too small for 42 pattern")
            return

        offset_x: int = (self.width - self.Pattern_width) // 2
        offset_y: int = (self.height - self.Pattern_height) // 2
        for px, py in self.Digit_4:
            self.pattern_cells.add((offset_x + px, offset_y + py))
        for px, py in self.Digit_2:
            self.pattern_cells.add((offset_x + 4 + px, offset_y + py))
        if self.entry_point in self.pattern_cells:
            print("Warning: entry overlaps 42 pattern, skipping pattern")
            self.pattern_cells.clear()
            return
        if self.exit_point in self.pattern_cells:
            print("Warning: exit overlaps 42 pattern, skipping pattern")
            self.pattern_cells.clear()
            return
        for px, py, in self.pattern_cells:
            self.grid[py][px].visited = True

    # -------------------------------------------------------------------------
    # Carve in the grid
    # -------------------------------------------------------------------------
    def remove_wall(self, cell_a: "MazeGenerator.Cell",
                    cell_b: "MazeGenerator.Cell") -> None:
        """Remove the shared wall between two adjacent cells."""
        dx: int = cell_b.x - cell_a.x
        dy: int = cell_b.y - cell_a.y

        if dx == 1 and dy == 0:
            cell_a.east = False
            cell_b.west = False
        elif dx == -1 and dy == 0:
            cell_a.west = False
            cell_b.east = False
        elif dx == 0 and dy == 1:
            cell_a.south = False
            cell_b.north = False
        elif dx == 0 and dy == -1:
            cell_a.north = False
            cell_b.south = False

    # -------------------------------------------------------------------------
    # Create hex output file
    # -------------------------------------------------------------------------
    def create_output_file(self, output_filename: str) -> None:
        """Solve the maze and write the result to a text file.

        Runs BFS to find the solution path, then writes the grid in
        hex format followed by entry, exit and solution path.
        """
        BFS_solver = self.BFS(self)
        path = BFS_solver.get_path_string()

        if BFS_solver.path is None:
            self.BFS()
        try:
            with open(output_filename, "w") as output_file:
                for row in self.grid:
                    output_file.write(f"{self.row_to_hex(row)}\n")
                output_file.write("\n")
                output_file.write(f"{self.entry_point[0]}, "
                                  f"{self.entry_point[1]}\n")
                output_file.write(f"{self.exit_point[0]}, "
                                  f"{self.exit_point[1]}\n")
                output_file.write(f"{path}\n")
                print(f"Maze successfully saved to '{output_filename}'!")
        except Exception as message:
            print(f"Error: output file: {message}")

    # -------------------------------------------------------------------------
    # Convert to hex
    # -------------------------------------------------------------------------
    def row_to_hex(self, maze_row: list[Cell]) -> str:
        """Convert a row of cells into a hex string encoding wall states.

        Each cell is encoded as a 4-bit value where each bit represents
        a wall: north=1, east=2, south=4, west=8. The bits are summed
        and formatted as a single hex character per cell.
        """
        bin_val: int = 0
        row_in_hex: str = ""

        for cell in maze_row:
            bin_val = 0
            if cell.north is True:
                bin_val += 1
            if cell.east is True:
                bin_val += 2
            if cell.south is True:
                bin_val += 4
            if cell.west is True:
                bin_val += 8
            row_in_hex += format(bin_val, "X")
        return row_in_hex

    # -------------------------------------------------------------------------
    # DFS Algorithm
    # -------------------------------------------------------------------------
    class DFS:
        """Generate a maze using Depth-First Search.

        Carves paths by exploring as far as possible before backtracking.
        Produces a perfect maze by default. If perfect is False, randomly
        removes extra walls after generation to create loops.
        """
        def __init__(self, maze: "MazeGenerator") -> None:
            """Initialize and run the DFS generation on the maze."""
            self.maze: MazeGenerator = maze
            self._generate()

        def _get_unvisited_neighbors(
                self, cell: "MazeGenerator.Cell"
        ) -> list["MazeGenerator.Cell"]:
            """Return all unvisited neighbors of a cell."""
            neighbors: list["MazeGenerator.Cell"] = []
            for dx, dy in self.maze.Directions.values():
                nx: int = cell.x + dx
                ny: int = cell.y + dy
                if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                    neighbor = self.maze.grid[ny][nx]
                    if not neighbor.visited:
                        neighbors.append(neighbor)
            return neighbors

        def _generate(self) -> None:
            """Run the iterative DFS to carve the maze paths.

            Starts from the entry point and uses a stack to backtrack
            when no unvisited neighbors remain.
            """
            start_x, start_y = self.maze.entry_point
            start_cell = self.maze.get_cell(start_x, start_y)
            start_cell.visited = True

            stack: list["MazeGenerator.Cell"] = [start_cell]

            while stack:
                current = stack[-1]
                neighbors = self._get_unvisited_neighbors(current)
                if neighbors:
                    chosen = random.choice(neighbors)
                    self.maze.remove_wall(current, chosen)
                    chosen.visited = True
                    stack.append(chosen)
                else:
                    stack.pop()
            if not self.maze.perfect:
                self._make_unperfect()

        def _make_unperfect(self) -> None:
            """Randomly remove walls to introduce loops in the maze.

            Skips pattern cells. Removes roughly 10% of remaining
            intact walls to create an imperfect maze.
            """
            walls: list[tuple["MazeGenerator.Cell", "MazeGenerator.Cell"]] = []
            for y in range(self.maze.height):
                for x in range(self.maze.width):
                    cell = self.maze.grid[y][x]
                    if (x, y) in self.maze.pattern_cells:
                        continue
                    if cell.east and x + 1 < self.maze.width:
                        neighbor = self.maze.grid[y][x + 1]
                        if (x + 1, y) not in self.maze.pattern_cells:
                            walls.append((cell, neighbor))
                    if cell.south and y + 1 < self.maze.height:
                        neighbor = self.maze.grid[y + 1][x]
                        if (x, y + 1) not in self.maze.pattern_cells:
                            walls.append((cell, neighbor))
            nb_to_remove = max(1, len(walls) // 10)
            chosen = random.sample(walls, min(nb_to_remove, len(walls)))
            for cell_a, cell_b in chosen:
                self.maze.remove_wall(cell_a, cell_b)

    # -------------------------------------------------------------------------
    # Eller Algorithm
    # -------------------------------------------------------------------------
    class Eller:
        """Generate a maze using Eller's algorithm.

        Processes the grid row by row, assigning set IDs to cells and
        randomly merging adjacent cells in the same row. Carves vertical
        connections downward ensuring every set has at least one passage
        to the next row. The last row forces all remaining sets to merge.
        """
        CellTuple = tuple[int, "MazeGenerator.Cell"]
        TupList = list[CellTuple]

        def __init__(self, maze: "MazeGenerator") -> None:
            """Initialize and run Eller's generation on the maze."""
            self.maze: MazeGenerator = maze
            self._generate()

        def _generate(self) -> None:
            """Run Eller's algorithm row by row across the grid.

            Handles horizontal and vertical carving for each row,
            then forces full merging on the last row.
            """
            self._reset_ids(self.maze.grid)
            for index, row in enumerate(self.maze.grid):
                if index + 1 < self.maze.height:
                    next_row = self.maze.grid[index + 1]
                    self._horizontal_row_carving(row, next_row)
                    self._vertical_row_carving(row, next_row)
                else:
                    self._horizontal_row_carving(row)
                    self._open_last_row(row)

        def _reset_ids(self, maze: list[list["MazeGenerator.Cell"]]) -> None:
            """Reset all cell set IDs to -1 before generation starts."""
            self.global_max_id = -1
            for row in maze:
                for cell in row:
                    cell.set_id = -1

        def _horizontal_row_carving(self,
                                    row: list["MazeGenerator.Cell"],
                                    next_row:
                                    Optional[list["MazeGenerator.Cell"]] =
                                    None) -> None:
            """Assign set IDs and randomly merge adjacent cells in a row.

            Cells without an ID are assigned a new unique one. Adjacent
            cells from different sets are randomly merged by removing the
            wall between them and unifying their set IDs.
            """
            max_id = max((cell.set_id for cell in row if cell.set_id >= 0),
                         default=-1)
            if max_id > self.global_max_id:
                self.global_max_id = max_id
            i = self.global_max_id + 1

            for cell in row:
                if cell.set_id == -1:
                    cell.set_id = i
                    i += 1
            for ix in range(len(row) - 1):
                cell_a = row[ix]
                cell_b = row[ix + 1]
                if cell_a.set_id != cell_b.set_id:
                    merging = random.random()
                    old_id = cell_b.set_id
                    if merging > 0.55:
                        cell_a.east = False
                        cell_b.west = False
                        for cell in row:
                            if cell.set_id == old_id:
                                cell.set_id = cell_a.set_id

        def _vertical_row_carving(self, row: list["MazeGenerator.Cell"],
                                  next_row:
                                  list["MazeGenerator.Cell"]) -> None:
            """Carve vertical passages from the current row to the next."""
            sets = defaultdict(list)
            for i, cell in enumerate(row):
                if not cell.visited:
                    sets[cell.set_id].append((i, cell))
            if self.maze.perfect:
                for set_id, set_list in sets.items():
                    to_open = random.choice(set_list)
                    self._open_vert(to_open, next_row)
            else:
                for set_id, set_item in sets.items():
                    k = randint(1, len(set_item))
                    sample = random.sample(set_item, k)
                    self._open_vert(sample, next_row)

        def _open_vert(self, to_open: Union[CellTuple, TupList],
                       next_row: list["MazeGenerator.Cell"]) -> None:
            """Open a vertical passage between a cell and the one below it.

            Handles both a single cell tuple and a list of cell tuples.
            Propagates the set ID downward to maintain set membership.
            """
            if isinstance(to_open, tuple):
                i, cell = to_open
                cell.south = False
                next_row[i].north = False
                next_row[i].set_id = cell.set_id
            else:
                for i, cell in to_open:
                    cell.south = False
                    next_row[i].north = False
                    next_row[i].set_id = cell.set_id

        def _open_last_row(self, row: list["MazeGenerator.Cell"]) -> None:
            """Merge all remaining sets in the last row.

            Removes walls between adjacent cells from different sets
            until the entire last row belongs to a single set, ensuring
            the maze has a valid solution path."""
            for ix in range(len(row) - 1):
                if row[ix].set_id != row[ix + 1].set_id:
                    new_id = row[ix].set_id
                    old_id = row[ix + 1].set_id
                    row[ix].east = False
                    row[ix + 1].west = False
                    for cell in row:
                        if cell.set_id == old_id:
                            cell.set_id = new_id

    # -------------------------------------------------------------------------
    # BFS Algorithm
    # -------------------------------------------------------------------------
    class BFS:
        """Solve the maze using Breadth-First Search.

        Finds the shortest path from the entry point to the exit point
        by exploring all reachable cells level by level, only crossing
        through open walls.
        """
        def __init__(self, maze: "MazeGenerator") -> None:
            """Initialize and run BFS on the given maze."""
            self.maze: MazeGenerator = maze
            self.path: list[str] = []
            self._find_path(maze)

        def _get_free_neighbors(self,
                                cell: "MazeGenerator.Cell"
                                ) -> list[tuple["MazeGenerator.Cell", str]]:
            """Return all neighbors reachable through open walls."""
            neighbors: list[tuple["MazeGenerator.Cell", str]] = []
            if not cell.north and cell.y > 0:
                neighbor = self.maze.grid[cell.y - 1][cell.x]
                neighbors.append((neighbor, "N"))
            if not cell.east and cell.x < self.maze.width - 1:
                neighbor = self.maze.grid[cell.y][cell.x + 1]
                neighbors.append((neighbor, "E"))
            if not cell.south and cell.y < self.maze.height - 1:
                neighbor = self.maze.grid[cell.y + 1][cell.x]
                neighbors.append((neighbor, "S"))
            if not cell.west and cell.x > 0:
                neighbor = self.maze.grid[cell.y][cell.x - 1]
                neighbors.append((neighbor, "W"))
            return neighbors

        def _find_path(self, maze: "MazeGenerator") -> None:
            """Run BFS from entry to exit and store the solution path.

            Explores cells in order using a queue. Records the sequence
            of directions taken to reach the exit. Prints an error if
            no path exists.
            """
            start_x, start_y = self.maze.entry_point
            start = self.maze.get_cell(start_x, start_y)
            end_x, end_y = self.maze.exit_point
            end = self.maze.get_cell(end_x, end_y)

            visited: set[tuple[int, int]] = set()
            visited.add((start.x, start.y))

            queue: deque[tuple["MazeGenerator.Cell", list[str]]] = deque()
            queue.append((start, []))
            while queue:
                current, path = queue.popleft()

                if current.x == end.x and current.y == end.y:
                    self.path = path
                    return
                for neighbor, direction in self._get_free_neighbors(current):
                    if (neighbor.x, neighbor.y) not in visited:
                        visited.add((neighbor.x, neighbor.y))
                        queue.append(
                            (neighbor, path + [direction])
                        )
            print("Error: no path found from entry to exit")

        def get_path_string(self) -> str:
            return "".join(self.path)
