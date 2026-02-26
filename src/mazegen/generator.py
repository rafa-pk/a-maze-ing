import sys
import random
from dataclasses import dataclass
from collections.abc import Callable
from collections import deque
from collections import defaultdict



class MazeGenerator:
    """"""
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

    @dataclass
    class Cell:
        x: int
        y: int
        north: bool = True
        east: bool = True
        south: bool = True
        west: bool = True
        visited: bool = False
        set_id: int = -1

    def __init__(self, width: int, height: int, 
                 entry_point: tuple[int, int], exit_point: tuple[int, int],
                 algo: str | None = None, seed: int | None = None) -> None:
        self.width = width
        self.height = height
        self.entry_point = entry_point
        self.exit_point = exit_point
        self.pattern_cells: set[tuple[int, int]] = set()
        if algo is None:
            self.algo = "DFS"
        else:
            self.algo = algo
        if seed is not None:
            self.seed = random.seed(seed)
        else:
            seed = random.randint(0, 2**32 - 1)
            self.seed = random.seed(seed)
        self.grid: list[list] = [
            [self.Cell(x=x, y=y) for x in range(self.width)]
            for y in range(self.height)
        ]
    
    def generate_maze(self, perfect: bool = True, 
                      visualizer: Callable[..., None] |None = None) -> None: 
        """""" 
        self.perfect = perfect
        self._place_42_pattern()
        if visualizer:
            visualizer()
        if self.algo == "DFS":
            self.DFS(self)
        elif self.algo == "Eller":
            self.Eller(self)

    def get_cell(self, x: int, y: int) -> object:
        return self.grid[y][x]

    def _place_42_pattern(self) -> None:
        if (self.width < self.Pattern_width
                or self.height < self.Pattern_height):
            print("Warning: maze too small for 42 pattern")
            return

        offset_x: int = (self.width - self.Min_width) // 2
        offset_y: int = (self.height - self.Min_height) // 2
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

    def remove_wall(self, cell_a, cell_b) -> None:
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
   
    #def _make_unperfect(self):
    #

    def create_output_file(self, output_filename: str) -> None:
       
        BFS_solver = self.BFS(self)
        path = BFS_solver.get_path_string()

        #if BFS_solver.path is None:
        #    self.BFS()
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

    def row_to_hex(self, maze_row: list[Cell]) -> str:
        bin_val: int = 0
        row_in_hex: str = ""

        for cell in maze_row:
            if cell.north == True:
                bin_val += 1
            if cell.east == True:
                bin_val += 2
            if cell.south == True:
                bin_val += 4
            if cell.west == True:
                bin_val += 8
            row_in_hex += format(bin_val, "X")
        return row_in_hex


    class DFS:
        def __init__(self, maze: "MazeGenerator") -> None:
            self.maze: MazeGenerator = maze
            self._generate()

        def _get_unvisited_neighbors(self, cell: object) -> list:
            neighbors: list = []
            for dx, dy in self.maze.Directions.values():
                nx: int = cell.x + dx
                ny: int = cell.y + dy
                if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                    neighbor = self.maze.grid[ny][nx]
                    if not neighbor.visited:
                        neighbors.append(neighbor)
            return neighbors

        def _generate(self) -> None:
            start_x, start_y = self.maze.entry_point
            start_cell = self.maze.get_cell(start_x, start_y)
            start_cell.visited = True

            stack: list = [start_cell]

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
            #if not self.maze.perfect:
            #    self.maze._make_unperfect()

    class Eller:
        CellTuple = tuple[int, "MazeGenerator.Cell"]
        TupList = list[CellTuple]

        def __init__(self, maze: "MazeGenerator") -> None:
            self.maze: MazeGenerator = maze
            self._generate()

        def _generate(self) -> None:
            self._reset_ids(self.maze.grid)
            for index, row in enumerate(self.maze.grid): 
                self._horizontal_row_carving(row)
                if index + 1 < self.maze.height:
                    next_row = self.maze.grid[index + 1]
                    self._vertical_row_carving(row, next_row)
                else:
                    self._open_last_row(row)
            
        def _reset_ids(self, maze: "MazeGenerator.grid") -> None:
            for row in maze:
                for cell in row:
                    if cell.visited:
                        cell.set_id = -2
                    cell.set_id = -1

        def _horizontal_row_carving(self,
                                     row: list["MazeGenerator.Cell"]) -> None:
            
            max_id = max((cell.set_id for cell in row), default=-1)
            i = max_id + 1
            ix = 0

            for cell in row:
                if cell.set_id == -1:
                    cell.set_id = i
                    i += 1
            for ix in range(len(row) - 1):
                cell_a = row[ix]
                cell_b = row[ix + 1]
                if cell_a.visited or cell_b.visited:
                    continue
                if cell_a.set_id != cell_b.set_id:
                    merging = random.random()
                    if merging > 0.7:
                        cell_a.east = False
                        cell_b.west = False
                        for cell in row:
                            if cell.set_id == cell_b.set_id: 
                                cell.set_id = cell_a.set_id

        def _vertical_row_carving(self, row: list["MazeGenerator.Cell"], 
                       next_row: list["MazeGenerator.Cell"]) -> None:
            sets = defaultdict(list)

            for i, cell in enumerate(row):
                if not cell.visited:
                    sets[cell.set_id].append((i, cell))
            if self.maze.perfect:
                for set_id, group in sets.items():
                    to_open = random.choice(group)
                    self._open_vert(to_open, next_row)
            else:
                for set_id, group in sets.items():
                    k = randint(1, len(group))
                    to_open = random.sample(group, k)
                    self._open_vert(to_open, next_row)


        def _open_vert(self, to_open: CellTuple | TupList,
                       next_row: list["MazeGenerator.Cell"],) -> None:
            if isinstance(to_open, tuple):
                i, cell = to_open
                cell.south = False
                if not next_row[i].visited:
                    next_row[i].north = False
                    next_row[i].set_id = cell.set_id
            else:
                for i, cell in to_open:
                    cell.south = False
                    if not next_row[i].visited:
                        next_row[i].north = False
                        next_row[i].set_id = cell.set_id

        def _open_last_row(self, row: list["MazeGenerator.Cell"]) -> None:
            for ix in range(len(row) - 1):
                if row[ix].set_id != row[ix + 1].set_id:
                    row[ix].east = False
                    row[ix + 1].west = False
                    for cell in row:
                        if cell.set_id == row[ix + 1].set_id:
                            cell.set_id = row[ix].set_id
     
    class BFS:
        def __init__(self, maze: "MazeGenerator") -> None:
            self.maze: MazeGenerator = maze
            self.path: list = []
            self._find_path(maze)

        def _get_free_neighbors(self, cell: object) -> list:
            neighbors: list = []
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

        def _find_path(self, maze):
            start_x, start_y = self.maze.entry_point
            start = self.maze.get_cell(start_x, start_y)
            end_x, end_y = self.maze.exit_point
            end = self.maze.get_cell(end_x, end_y)

            visited: set = set()
            visited.add((start.x, start.y))

            queue: deque = deque()
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

    def print_grid(self, path: list = None) -> None:
        path_cells: set = set()
        if path:
            cx, cy = self.entry
            path_cells.add((cx, cy))
            for direction in path:
                dx, dy = self.Directions[direction]
                cx += dx
                cy += dy
                path_cells.add((cx, cy))

        for y in range(self.height):
            top: str = ""
            mid: str = ""
            for x in range(self.width):
                cell = self.grid[y][x]
                top += "+" + ("---" if cell.north else "   ")
                mid += ("|" if cell.west else " ")
                if (x, y) == self.entry_point:
                    mid += " E "
                elif (x, y) == self.exit_point:
                    mid += " X "
                elif (cell.x, cell.y) in self.pattern_cells:
                    mid += " # "
                elif (x, y) in path_cells:
                    mid += " ` "
                else:
                    mid += "   "
            top += "+"
            mid += "|" if self.grid[y][self.width - 1].east else " "
            print(top)
            print(mid)
        bottom: str = ""
        for x in range(self.width):
            cell = self.grid[self.height - 1][x]
            bottom += "+" + ("---" if cell.south else "   ")
        bottom += "+"
        print(bottom)
