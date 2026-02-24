from typing import Any, List, Dict, Tuple, Set
import random


class MazeGrid:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height 
        self.grid: List[int] = []
        self.stack: List[Tuple[int, int]] = []
        self.visited: Set[Tuple[int, int]] = set()
        self.directions: Dict[int, Tuple[int, int]] = {
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

    def generate(self, entry: Tuple[int, int]) -> None:
        # Ensure a fresh start
        self.stack = []
        self.visited = set()

        # Initialize the starting point (Entry)
        self.stack.append(entry)
        self.visited.add(entry)

        while self.stack:
            # 1. Look at the current cell (the Top of the stack)
            curr_x, curr_y = self.stack[-1]
            
            # 2. Find all unvisited neighbors
            neighbors = []
            
            # Here is where we will use your self.directions!
            for wall, (dx, dy) in self.directions.items():

                nx, ny = curr_x + dx, curr_y + dy

                # Check boundaries and if visited
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.visited:
                    neighbors.append((wall, nx, ny))

            if neighbors:
                # SCENARIO A: We have somewhere to go!
                # Pick one randomly
                wall, nx, ny = random.choice(neighbors)
                
                # CARVE: Remove the wall from current and opposite from neighbor
                self.grid[curr_y][curr_x] -= wall
                self.grid[ny][nx] -= self.opposites[wall]
                
                # MOVE: Add to visited and push to stack
                self.visited.add((nx, ny))
                self.stack.append((nx, ny))
            else:
                # SCENARIO B: Dead end! 
                # Backtrack by removing the current room from the stack
                self.stack.pop()

    def save_to_file(self, filename: str) -> None:
        """
        Exports the grid data to a text file.
        Each line represents a row, with wall values separated by spaces.
        """
        try:
            with open(filename, 'w') as f:
                for row in self.grid:
                    # Convert [11, 13, 1] -> "11 13 1"
                    line = " ".join(map(str, row))
                    f.write(line + "\n")
            print(f"Successfully saved maze to {filename}")
        except IOError as e:
            # Centralized error handling as per Operating Directives
            print(f"Critical: Failed to write maze data. {e}")


    def set_boundaries(self, entry: Tuple[int, int], exit_coords: Tuple[int, int]) -> None:
        """
        Finalizes the maze by opening the entry and exit walls.
        Ensures compliance with subject requirements for access points.
        """
        # entry_x, entry_y
        ex, ey = entry
        # exit_x, exit_y
        xx, xy = exit_coords

        # Guard against out-of-bounds before bit manipulation
        if (0 <= ex < self.width and 0 <= ey < self.height and 
            0 <= xx < self.width and 0 <= xy < self.height):
            
            # Use bitwise AND NOT to safely clear the bits
            # North (1) for Entry, South (4) for Exit
            self.grid[ey][ex] &= ~1
            self.grid[xy][xx] &= ~4
        else:
            # Resilient Design: Log error instead of crashing
            print("Warning: Entry or Exit coordinates are out of grid bounds.")
