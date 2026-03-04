from typing import List, Tuple, Dict
from mazegen.cell import Cell


OPPOSITE: Dict[str, str] = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E"
}


class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height

        self.cells: List[List[Cell]] = [[Cell(x, y) for x in range(width)] for y in range(height)]


    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]

    def in_bounds(self, x: int, y: int) -> bool:
        x_in_bounds: bool = x >= 0 and x < self.width
        y_in_bounds: bool = y >= 0 and y < self.height

        return x_in_bounds and y_in_bounds


    def get_neighbors(self, cell: Cell) -> List[Tuple[str, Cell]]:

        directions: Dict[str, Tuple[int, int]] = {
            "N": (cell.x, cell.y - 1),
            "E": (cell.x + 1, cell.y),
            "S": (cell.x, cell.y + 1),
            "W": (cell.x - 1, cell.y)
        }
        neighbors: List[Tuple[str, Cell]] = []

        for key, (x, y) in directions.items():
            if self.in_bounds(x, y):
                neighbor: Cell = self.cells[y][x]
                neighbors.append((key, neighbor))

        return neighbors

    def open_wall(self, cell: Cell, neighbor: Cell, direction: str) -> None:
        cell.walls[direction] = True
        neighbor.walls[OPPOSITE[direction]] = True
