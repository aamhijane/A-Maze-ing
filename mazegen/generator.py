from typing import List, Tuple
from collections import deque
from mazegen.grid import Grid
from mazegen.cell import Cell

import random


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int | None, perfect: bool, entry_point: Tuple[int, int], exit_point: Tuple[int, int]) -> None:
        self.width: int = width
        self.height: int = height
        self.seed: int | None = seed
        self.perfect: bool = perfect
        self.entry_point: Tuple[int, int] = entry_point
        self.exit_point: Tuple[int, int] = exit_point

        # Apply seed
        if self.seed is not None:
            random.seed(self.seed)

        # Create Grid
        self.grid = Grid(self.width, self.height)

        # Initialize stack with entry cell & marked as visited
        self.stack: List[Cell] = [self.grid.get_cell(self.entry_point[0], self.entry_point[1])]
        self.stack[0].visited = True

        # Generate
        self._generate()


    def _generate(self) -> None:

        # Loop until stack is empty.
        while self.stack:

            # Get unvisited neighbors
            unvisited_neighbors: List[Tuple[str, Cell]] = self._get_unvisited_neighbors(self.stack[-1])

            # If any exist
            if unvisited_neighbors:

                # Pick unvisited neighbor randomly
                direction, neighbor = random.choice(unvisited_neighbors)

                # Open wall
                self.grid.open_wall(self.stack[-1], neighbor, direction)

                # Mark as visited
                neighbor.visited = True

                # Push to stack
                self.stack.append(neighbor)

            # If none
            else:

                # Pop from stack
                self.stack.pop()


    def _get_unvisited_neighbors(self, cell: Cell) -> List[Tuple[str, Cell]]:
        unvisited: List[Tuple[str, Cell]] = [
            (direction, neighbor)
            for direction, neighbor in self.grid.get_neighbors(cell)
            if not neighbor.visited
        ]

        return unvisited


    def solve(self) -> str:

        # Start at entry, empty path
        entry: Cell = self.grid.get_cell(self.entry_point[0], self.entry_point[1])
        exit_cell: Cell = self.grid.get_cell(self.exit_point[0], self.exit_point[1])

        # Queue holds (current_cell, path_so_far)
        queue: deque = deque()
        queue.append((entry, []))

        # Track visited cells to avoid loops
        visited: set[Cell] = {entry}

        while queue:

            # 1. Pop from the FRONT
            current, path = queue.popleft()

            # 2. Did we reach the exit?
            if current == exit_cell:
                return "".join(path)

            # 3. Explore open neighbors
            for direction, neighbor in self.grid.get_neighbors(current):

                # 4. Check: is the wall open? (remember your analogy)
                if current.walls[direction]:

                    # 5. Check: not visited yet?
                    if neighbor not in visited:

                        # 6. Mark visited
                        visited.add(neighbor)

                        # 7. Add to queue with extended path
                        queue.append((neighbor, path + [direction]))

        # No path found
        return ""
