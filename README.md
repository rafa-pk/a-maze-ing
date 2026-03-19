*This project has been created as part of the 42 curriculum by amaazouz and rvaz-da-.*


---

# A-Maze-Ing

## Description

> **Goal:** The aim of this project is to build a python-based maze generator and a graphical interface for it, allowing for a deep dive into algorithms, graph theory and graphics programming.

The program parses maze parameters from a configuration file, in order to generate an either perfect or non-perfect maze — perfect meaning having exactly one unique path between any two points.
The maze gets output to a file in a hexadecimal wall representation and graphically represented to a graphical window via MLX library. The graphical interface also includes some user interactions, such asdisplaying/not displaying the solution path, changing maze colors, adding animation...

### Maze Generation Algorithm

**Algorithm choice:** Recursive Backtracking (BFS), Eller's

**How they work:**
Our main algorithm is BFS, which is a graph traversal algorithm. It starts from the entry point and it visits all cells adjacent to the entry. Then moves on to visiting the adjacent cells of the previously visited cells, and continues to do so until everything has been visited.
Eller's algorithm works in a very different way, it is a set theory-based algorithm. It generates the maze line by line, by randomly merging adjacent sets and randomly opening a downward wall per set. It allows for infinitely large maze generation in linear time.

**Why we chose them:**
The BFS algorithm came quite naturally, having a very nice difficulty to efficiency ratio. It is a quite easy to implement algorithm, which works very well. We thought we'd first secure the mandatory part with it. The Eller's algorithm came in an attempt to learn and implement a new algorithm, we hesitated between Eller's and Kruskal, but Eller's looked both cooler and harder, which were the defining factors. Of course, its efficiency is also a positive point.

---

## Config File

> Structure and format of the configuration file used:


| Field | Example | Description |
|-------|---------|-------------|
| `WIDTH` | `80` | maze width, number of horizontal cells |
| `HEIGHT` | `80` | maze height, number of vertical cells |
| `ENTRY` | `24,9` | coordinates of maze entry (x,y) |
| `EXIT` | `67,58` | coordinates of maze exit (x,y) |
| `OUTPUT_FILE` | `maze.txt` | filename of hex output |
| `PERFECT` | `True` | perfect/non-perfect maze toggle |
| `ALGORITHM` |  `Eller` | (optional) choice of algorithm, defaults to BFS |
| `SEED` | `80` | (optional) seed for reproducibility |

Algorithm and seed entries do not need to be in the config file and are optional.

---

## Instructions

### Usage

```bash
make install        # Installs virtual environment and all needed dependencies

make run            # Runs the program

make lint           # Verifies flake8 and mypy norm conventions

make clean          # Cleans cache files

make build          # Creates .whl package
```

### Execution

```bash
python3 <config_file>
```

**Actions**

When the program gets run, multiple actions are available to interact with the MLX window:
| Key | Behaviour |
|-------|---------|
| `ESC` |Exit the window and terminate the program. |
| `1` |Toggles between displaying path and not displaying path |
| `2` | Generates new maze |
| `3` | Switches between the available maze themes |
| `4` | Switches between algorithms and generates new maze |
| `5` | Displays path with animations |


---

## Features

- [x] Maze generation with BFS
- [x] Path-finding algorithm with DFS
- [x] Graphical window management
- [x] *(Advanced)* Second maze generation algorithm
- [x] *(Advanced)* Maze path animations on display
- [x] *(Advanced)* Extra interaction keys
- [x] *(Advanced)* Extra colors and 42 logo color shift


---

## Reusable Code

To ensure modularity, the core maze generation logic is isolated in a separate package named mazegen, located in the packages directory of the project. This package can be built into .whl/.tar.gz and installed via pip.
How to use?

```
from mazegen import MazeGenerator

# Instantiate the generator
generator = MazeGenerator(<settings>)

# Generate and access structure
maze = generator.generate_maze()
solution = generator.DFS()

```

---

## Team & Project Management

### Team Members

| Login | Roles |
|-------|---------|
| rvaz-da- | BFS, DFS, graphical bonuses, norm-compliance |
| amaazouz | Parsing, Eller's algorithm, README.md |

### Planning

**Anticipated plan:**
We did not really plan enough at the beginning, we thought of firstly just take care of the base algorithms and logic, and only after thinkign about MLX and bonuses.

**How it evolved:**
We did not think project structure and intentions enough, so we ended up having to refactor our codebase's structure multiple times to account for changes. Especially before implementing MLX.

### Retrospective

**What worked well:**
- Good communication and splitting of tasks.

**What could be improved:**
- Further anticipation of project structure.
- More parallel work

---

## Resources

### Documentation & References

- [W3 Schools](https://www.w3schools.com) — General python information
- [GeeksforGeeks](https://www.geeksforgeeks.org) — General python information
- [Maze Generation Algorithms - An Exploration](https://professor-l.github.io/mazes/) — Introductory article to maze generators
- [Breadth-first search](https://cp-algorithms.com/graph/breadth-first-search.html) - Article about BFS algorithm
- [Depth First Search](https://cp-algorithms.com/graph/depth-first-search.html) - Article about DFS algorithm
- [Depth-First Search (DFS) Algorithm](https://medium.com/@that-software-PM/depth-first-search-dfs-algorithm-201dc95e524) - Medium article about DFS
- [Maze Generation: Eller's Algorithm](https://weblog.jamisbuck.org/2010/12/29/maze-generation-eller-s-algorithm) - Blog article about Eller's algorithm
- [Eller's Algorithm](http://www.neocomputer.org/projects/eller.html) - Blog article about Eller's algorithm
- [Eller’s Maze Algorithm in JavaScript](https://cantwell-tom.medium.com/ellers-maze-algorithm-in-javascript-2e5742c1a4cd) - Medium article about Eller's algorithm implementation
- [MiniLibX Guide](https://harm-smits.github.io/42docs/libs/minilibx) - 42 student made guide to MLX
- [MiniLibX](https://42-cursus.gitbook.io/guide/minilibx) - Guide for MiniLibX


### AI Usage

Copilot, Gemini, Claude and Mistral were used for this project. No tasks were delegated to AI, it was mainly used to ask specific questions on some topics and to understand error messages. It may also have been used to get logic ideas, but none were actually used at the end. 
We also asked AI to make output tester functions before MLX was implemented.
