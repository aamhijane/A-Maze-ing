import random
from typing import List, Tuple, Optional
from collections import deque
from mazegen.grid import Grid
from mazegen.cell import Cell
from mazegen.grid import OPPOSITE

# 42 pattern
PATTERN_42: List[List[int]] = [
    [1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]


class MazeGenerator:
    """Generate a maze using the recursive backtracker (DFS) algorithm.

    Attributes:
        width (int): Number of columns in the maze.
        height (int): Number of rows in the maze.
        seed (Optional[int]): Random seed for reproducibility.
        perfect (bool): Whether the maze should be a perfect maze.
        entry_point (Tuple[int, int]): Entry coordinates (x, y).
        exit_point (Tuple[int, int]): Exit coordinates (x, y).
        grid (Grid): The generated maze grid.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int],
        perfect: bool,
        entry_point: Tuple[int, int],
        exit_point: Tuple[int, int]
    ) -> None:
        """Initialize and generate the maze.

        Args:
            width (int): Number of columns in the maze.
            height (int): Number of rows in the maze.
            seed (Optional[int]): Random seed for reproducibility.
            perfect (bool): Whether to generate a perfect maze.
            entry_point (Tuple[int, int]): Entry cell coordinates (x, y).
            exit_point (Tuple[int, int]): Exit cell coordinates (x, y).
        """
        self.width: int = width
        self.height: int = height
        self.seed: Optional[int] = seed
        self.perfect: bool = perfect
        self.entry_point: Tuple[int, int] = entry_point
        self.exit_point: Tuple[int, int] = exit_point
        if self.seed is not None:
            random.seed(self.seed)
        self.grid: Grid = Grid(self.width, self.height)

        self.stack: List[Cell] = [
            self.grid.get_cell(self.entry_point[0], self.entry_point[1])
        ]
        self.stack[0].visited = True
        self.is_small = True
        if self.height >= len(PATTERN_42) and self.width >= len(PATTERN_42[0]):
            self._embed_42()
            self.is_small = False
        self._generate()

        if not self.perfect:
            self._add_loops()

    def _generate(self) -> None:
        """Generate the maze using the recursive backtracker algorithm.

        Carves passages by visiting unvisited neighbors randomly,
        backtracking when no unvisited neighbors remain.
        """
        while self.stack:
            unvisited_neighbors: List[Tuple[str, Cell]] = (
                self._get_unvisited_neighbors(self.stack[-1])
            )

            if unvisited_neighbors:
                direction, neighbor = random.choice(unvisited_neighbors)
                self.grid.open_wall(self.stack[-1], neighbor, direction)
                neighbor.visited = True
                self.stack.append(neighbor)
            else:
                self.stack.pop()

    def _is_3x3_open(self, top_x: int, top_y: int) -> bool:
        """Check if a 3x3 block starting at (top_x, top_y) is fully open.

        Uses BFS flood fill. If all 9 cells are reachable from the
        top-left cell through open walls, the block is fully open.

        Args:
            top_x (int): Left column of the 3x3 block.
            top_y (int): Top row of the 3x3 block.

        Returns:
            bool: True if all 9 cells are mutually reachable.
        """
        start: Cell = self.grid.get_cell(top_x, top_y)
        visited: set[Cell] = {start}
        queue: deque[Cell] = deque([start])

        while queue:
            current = queue.popleft()
            for direction, neighbor in self.grid.get_neighbors(current):
                if (neighbor not in visited
                        and top_x <= neighbor.x < top_x + 3
                        and top_y <= neighbor.y < top_y + 3
                        and not current.walls[direction]):
                    visited.add(neighbor)
                    queue.append(neighbor)

        return len(visited) == 9

    def _has_open_area(
        self, cell: Cell, neighbor: Cell, direction: str
    ) -> bool:
        """Check if opening a wall would create a 3x3 fully open area.

        Temporarily opens the wall, checks all nearby 3x3 blocks
        using BFS flood fill, then reverts the change.

        Args:
            cell (Cell): The origin cell.
            neighbor (Cell): The neighboring cell.
            direction (str): Direction of the wall to open.

        Returns:
            bool: True if opening this wall would create a 3x3 open area.
        """
        # Step 1: temporarily open the wall
        cell.walls[direction] = True
        neighbor.walls[OPPOSITE[direction]] = True

        found: bool = False

        # Step 2: check only 3x3 blocks that contain both cells
        min_x: int = max(0, min(cell.x, neighbor.x) - 2)
        max_x: int = min(self.width - 3, max(cell.x, neighbor.x))
        min_y: int = max(0, min(cell.y, neighbor.y) - 2)
        max_y: int = min(self.height - 3, max(cell.y, neighbor.y))

        for top_x in range(min_x, max_x + 1):
            for top_y in range(min_y, max_y + 1):
                if self._is_3x3_open(top_x, top_y):
                    found = True
                    break
            if found:
                break

        # Step 3: revert
        cell.walls[direction] = False
        neighbor.walls[OPPOSITE[direction]] = False

        return found

    def _add_loops(self) -> None:
        """Add random loops to the maze by removing extra walls.

        Randomly opens walls between adjacent cells to create cycles,
        making the maze imperfect (multiple paths between some cells).
        The number of loops is proportional to the maze size.
        """
        num_loops: int = (self.width * self.height) // 10
        attempts: int = 0
        max_attempts: int = num_loops * 10

        while attempts < max_attempts and num_loops > 0:
            x: int = random.randint(0, self.width - 2)
            y: int = random.randint(0, self.height - 2)
            direction: str = random.choice(["E", "S"])

            cell: Cell = self.grid.get_cell(x, y)
            dx, dy = (1, 0) if direction == "E" else (0, 1)
            neighbor: Cell = self.grid.get_cell(x + dx, y + dy)

            # Only open if both cells are NOT part of the "42" pattern
            if (not cell.walls[direction] and
                    any(cell.walls.values()) and
                    any(neighbor.walls.values()) and
                    not self._has_open_area(cell, neighbor, direction)):
                self.grid.open_wall(cell, neighbor, direction)
                num_loops -= 1

            attempts += 1

    def _embed_42(self) -> None:
        """Embed a '42' pattern of fully closed cells into the maze.

        Cells forming the '42' shape have all walls closed (hex 'F').
        Neighboring cells also have their wall pointing toward a '42'
        cell forced closed, preventing the generator from carving into it.
        Prints an error and skips if the maze is too small to fit the pattern.
        """
        pattern_h: int = len(PATTERN_42)
        pattern_w: int = len(PATTERN_42[0])

        self.start_x: int = (self.width - pattern_w) // 2
        self.start_y: int = (self.height - pattern_h) // 2

        for row_i, row in enumerate(PATTERN_42):
            for col_i, cell_val in enumerate(row):
                if cell_val == 1:
                    cell: Cell = self.grid.get_cell(
                        self.start_x + col_i,
                        self.start_y + row_i
                    )
                    # Force all walls closed on the "42" cell
                    cell.walls = {
                        "N": False,
                        "E": False,
                        "S": False,
                        "W": False
                    }
                    cell.visited = True

                    # Close the neighbor's wall pointing toward this cell
                    for direction, neighbor in self.grid.get_neighbors(cell):
                        neighbor.walls[OPPOSITE[direction]] = False

    def _get_unvisited_neighbors(self, cell: Cell) -> List[Tuple[str, Cell]]:
        """Return all unvisited neighbors of a given cell.

        Args:
            cell (Cell): The cell to check neighbors for.

        Returns:
            List[Tuple[str, Cell]]: List of (direction, neighbor) pairs
                where the neighbor has not yet been visited.
        """
        return [
            (direction, neighbor)
            for direction, neighbor in self.grid.get_neighbors(cell)
            if not neighbor.visited
        ]

    def solve(self) -> str:
        """Find the shortest path from entry to exit using BFS.

        Returns:
            str: A string of direction characters (N/E/S/W) representing
                the shortest path. Returns an empty string if no path exists.
        """
        entry: Cell = self.grid.get_cell(
            self.entry_point[0], self.entry_point[1]
        )
        exit_cell: Cell = self.grid.get_cell(
            self.exit_point[0], self.exit_point[1]
        )

        queue: deque[Tuple[Cell, List[str]]] = deque()
        queue.append((entry, []))
        visited: set[Cell] = {entry}

        while queue:
            current, path = queue.popleft()

            if current == exit_cell:
                return "".join(path)

            for direction, neighbor in self.grid.get_neighbors(current):
                if current.walls[direction] and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [direction]))

        return ""
