from typing import List, Tuple, Any
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
        self.stack: List[Cell] = [self.grid.get_cell(entry_point[0], entry_point[1])]
        self.stack[0].visited = True

        # Generate
        self._generate()


    def _generate(self) -> None:
        pass


    def _get_unvisited_neighbors(self, cell: Cell) -> List[Tuple[str, Cell]]:
        
        unvisited: List[Tuple[str, Cell]] = [
            (direction, neighbor)
            for direction, neighbor in self.grid.get_neighbors(cell)
            if not neighbor.visited
        ]

        return unvisited
