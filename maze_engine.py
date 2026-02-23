from typing import Any, List, Dict

class MazeGrid:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height 
        self.grid: List[int] = []
        self.directions: Dict[int, tuple] = {
            1: (0, -1),
            2: (1, 0),
            4: (0, 1),
            8: (-1, 0),
        }
        self.opposites: Dict[int, int] = {
            1: 4,
            2: 8,
            4: 1,
            8: 2,
        }
        self.create_grid()


    def create_grid(self) -> None:
        self.grid = [[15 for x in range(self.width)] for y in range(self.height)]

