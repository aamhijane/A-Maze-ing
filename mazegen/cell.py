from typing import Dict


class Cell:
    """Represent a single cell in a maze grid.

    Each cell tracks its position, the state of its four walls,
    and whether it has been visited during maze generation.

    Attributes:
        x (int): The horizontal position of the cell in the grid.
        y (int): The vertical position of the cell in the grid.
        walls (Dict[str, bool]): Wall states keyed by direction
            ('N', 'E', 'S', 'W'). True means open, False means closed.
        visited (bool): Whether this cell has been visited
            during maze generation.
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialize a Cell at position (x, y) with all walls closed.

        Args:
            x (int): The horizontal position of the cell.
            y (int): The vertical position of the cell.
        """
        self.x: int = x
        self.y: int = y
        self.walls: Dict[str, bool] = {
            "N": False,
            "E": False,
            "S": False,
            "W": False,
        }
        self.visited: bool = False

    def to_hex(self) -> str:
        '''Convert the cell's wall configuration
        to a single hexadecimal character.'''

        hex_chars = "0123456789ABCDEF"
        value = 0
        if self.walls["N"]:
            value += 1
        if self.walls["E"]:
            value += 2
        if self.walls["S"]:
            value += 4
        if self.walls["W"]:
            value += 8
        return hex_chars[15 - value]
