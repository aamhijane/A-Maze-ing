*This project has been created as part of the 42 curriculum by [ikelmouh], [ayamhija].*

---

# A-Maze-ing 🌀

![A-Maze-ing banner](https://raw.githubusercontent.com/aamhijane/A-Maze-ing/refs/heads/main/A-Maze-ing_banner.png)

## Description

A-Maze-ing is a maze generator and solver written in Python. The goal of the project is to procedurally generate mazes from a configuration file, solve them using a pathfinding algorithm, and display the result interactively in the terminal.

The program embeds a hidden **"42" pattern** of solid walls at the center of every maze large enough to contain it — a signature of the 42 school curriculum. Mazes can be either **perfect** (one unique path between any two cells) or **imperfect** (multiple paths via added loops). The solution is computed automatically and both the maze and its solution are written to an output file.

---

## Instructions

### Requirements

- Python 3.10 or higher
- pip / pip3
- flake8 / mypy

### Installation

**Using a virtual environment (recommended):**

```bash
make venv
source .venv/bin/activate
make install
```

**Using the global environment:**

```bash
make install
```

### Running the program

```bash
make run
```

This runs the program with the default `config.txt` file. To use a custom config:

```bash
python3 a_maze_ing.py your_config.txt
```

### Other Makefile targets

| Command | Description |
|---|---|
| `make venv` | Create and activate the local virtual environment |
| `make install` | Install dependencies from `requirements.txt` |
| `make run` | Run the program with `config.txt` |
| `make debug` | Run the program under `pdb` debugger |
| `make build` | Build the `mazegen` package |
| `make lint` | Run `flake8` + `mypy` type checking |
| `make lint_strict` | Run `mypy` in strict mode |
| `make clean` | Remove cache directories |

---

## Configuration File

The config file is a plain text file (`.txt`) containing `KEY=VALUE` pairs, one per line. Lines starting with `#` and blank lines are ignored.

### Full structure

```
# MANDATORY
WIDTH=13
HEIGHT=13
ENTRY=0,0
EXIT=12,12
OUTPUT_FILE=maze.txt
PERFECT=True

# OPTIONAL
SEED=42
ALGORITHM=recursive_backtracker
```

### Key reference

| Key | Type | Required | Description |
|---|---|---|---|
| `WIDTH` | Integer ≥ 1 | ✅ | Number of columns in the maze |
| `HEIGHT` | Integer ≥ 1 | ✅ | Number of rows in the maze |
| `ENTRY` | `x,y` | ✅ | Entry cell coordinates (0-indexed) |
| `EXIT` | `x,y` | ✅ | Exit cell coordinates (0-indexed) |
| `OUTPUT_FILE` | `.txt` filename | ✅ | Path to write the maze output |
| `PERFECT` | `True` / `False` | ✅ | Whether the maze has a unique solution |
| `SEED` | Integer | ❌ | Random seed for reproducibility |
| `ALGORITHM` | String | ❌ | Generation algorithm (see below) |

### Rules

- `ENTRY` and `EXIT` must be different coordinates.
- Both must be within the bounds of `WIDTH` and `HEIGHT`.
- `OUTPUT_FILE` must have a `.txt` extension.
- If `WIDTH` or `HEIGHT` is too small to embed the 42 pattern (< 9 columns or < 9 rows), the pattern is skipped.

---

## Maze Generation Algorithm

### Generation — Recursive Backtracker (DFS)

The maze is built using the **Recursive Backtracker** algorithm, an iterative depth-first search (DFS) over the grid:

1. Start at the entry cell and push it onto a stack.
2. Look at the top cell's unvisited neighbors.
3. If any exist, pick one randomly, carve a passage to it, mark it visited, and push it onto the stack.
4. If none exist, backtrack by popping the stack.
5. Repeat until the stack is empty — every reachable cell has been visited.

The result is a **perfect maze**: exactly one path exists between any two cells, with no loops and no isolated regions.

If `PERFECT=False`, extra walls are randomly removed after generation to introduce loops (multiple paths), with a guard that prevents the creation of fully open 3×3 areas.

### Pathfinding — BFS Solver

The maze is solved using **Breadth-First Search (BFS)**:

1. Start from the entry cell with an empty path.
2. Expand outward level by level through open walls.
3. The first time the exit cell is reached, the path taken is guaranteed to be the shortest.
4. The path is returned as a string of directions: `N`, `E`, `S`, `W`.

### Why this algorithm?

DFS was chosen for generation because it naturally produces **long, winding corridors** with a single correct solution — a classic maze feel. It is simple to implement iteratively, memory-efficient, and produces visually interesting mazes.

BFS was chosen for solving because it **guarantees the shortest path** in an unweighted grid, unlike DFS which can wander into dead ends.

---

## Reusable Components

The `mazegen` package (located in the `mazegen/` directory) is fully decoupled from the main script and can be installed and reused independently in any Python project.

### Installation as a package

```bash
pip install .
```

### Usage

```python
from mazegen import MazeGenerator, MazeWriter

maze = MazeGenerator(
    width=20,
    height=15,
    seed=42,
    perfect=True,
    entry_point=(0, 0),
    exit_point=(19, 14)
)

solution = maze.solve()   # returns e.g. "SSSEEENNN..."
print(solution)

writer = MazeWriter(maze, "output.txt")
writer.write()
```

### What is reusable

| Module | Description |
|---|---|
| `mazegen.generator.MazeGenerator` | Full maze generation + BFS solver |
| `mazegen.writer.MazeWriter` | Writes maze + solution to a `.txt` file |
| `mazegen.grid.Grid` | 2D cell grid with neighbor lookup |
| `mazegen.cell.Cell` | Individual cell with hex-encoded wall state |
| `mazegen.errors` | Custom exception hierarchy for clean error handling |

---

## Display

The maze is rendered interactively in the terminal using Python's built-in `curses` library (handled by `display.py` and `ikelmouh`).

**Features:**
- The maze walls are drawn using Unicode box-drawing characters for a clean visual.
- The solution path is animated/highlighted directly in the terminal.
- The display adapts to the terminal window size.
- No external display library is required — `curses` is part of the Python standard library.

---

## Team & Project Management

### Roles

| Member | Role |
|---|---|
| **ikelmouh** | Terminal display (`display.py`) — curses rendering, path animation, visual output |
| **ayamhija** | Everything else — maze generation, BFS solver, config parsing & validation, file I/O, error handling, package structure, Makefile |

### Planning

The project was split into two parallel tracks from the start:

- **Week 1:** Core maze generation (DFS algorithm, grid, cell encoding) + config parsing and validation.
- **Week 2:** BFS solver, MazeWriter output, error handling, and package structure (`pyproject.toml`).
- **Week 3:** Terminal display with curses, integration, testing, and README.

In practice, integration between the display and the generator took more time than anticipated, as the curses display needed access to the internal grid structure. This was resolved by passing the full `MazeGenerator` object directly to the display function.

### What worked well

- Separating the `mazegen` package from the main script made testing and reuse straightforward.
- The hex encoding of cell wall states (`cell.to_hex()`) kept the output file compact and easy to parse.
- Using a clean custom exception hierarchy made error messages consistent throughout.

### What could be improved

- The display could support mouse interaction or arrow-key navigation for an interactive solve mode.
- Additional generation algorithms (Prim's, Kruskal's) could be added behind the existing `ALGORITHM` config key.
- Unit test coverage could be expanded, especially for edge cases in config validation.

### Tools used

| Tool | Purpose |
|---|---|
| Python 3.10+ | Main language |
| `curses` | Terminal display |
| `mypy` | Static type checking |
| `flake8` | Code style linting |
| `pytest` | Unit testing |
| `make` | Build and task automation |
| Git | Version control |
| Claude (Anthropic AI) | Documentation writing, code explanation, debugging assistance, README generation |

---

## Resources

### Maze generation

- [Maze Generation Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker — Jamis Buck's blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [Buckblog: Maze Algorithms Overview](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)

### Pathfinding

- [Breadth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [BFS Pathfinding Explained — Red Blob Games](https://www.redblobgames.com/pathfinding/a-star/introduction.html)

### Python & curses

- [Python curses documentation](https://docs.python.org/3/library/curses.html)
- [Curses programming with Python — Python HOWTO](https://docs.python.org/3/howto/curses.html)
