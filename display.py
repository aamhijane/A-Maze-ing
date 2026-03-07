from mazegen.cell import Cell
from mazegen import MazeGenerator
import curses

type Win = curses.window


# def create_cell(cell: Cell) -> str:
#     cell_char = "▓"

#     W = cell.walls["W"]
#     E = cell.walls["E"]
#     N = cell.walls["N"]
#     S = cell.walls["S"]

#     top = ""
#     mid = ""
#     bot = ""

#     top += (cell_char if W == False else " ")
#     top += (cell_char * 2 if N == False else "  ")
#     top += (cell_char if E == False else " ") + "\n"

#     mid += (cell_char if W == False else " ")
#     mid += "  "
#     mid += (cell_char if E == False else " ") + "\n"

#     bot += (cell_char if W == False else " ")
#     bot += (cell_char * 2 if S == False else "  ")
#     bot += (cell_char if E == False else " ") + "\n"

#     return top + mid + bot


class Display:
    stdscr: Win

    def __init__(self, stdscr: Win) -> None:
        self.stdscr = stdscr

    def center_text(self, texte: str):
        height, width = self.stdscr.getmaxyx()
        lignes = texte.split("\n")
        start_y = max((height - len(lignes)) // 2, 0)

        for i, ligne in enumerate(lignes):
            x = max((width - len(ligne)) // 2, 0)
            if start_y + i < height:
                self.stdscr.addstr(start_y + i, x, ligne[:width-1])

    def _create_grid(self, maze: MazeGenerator) -> str:
        H = maze.grid.height
        W = maze.grid.width

        wall_char = "█"
        rows = H * 2 + 1
        cols = W * 2 + 1

        grid = [[wall_char for _ in range(cols)] for _ in range(rows)]

        for y in range(H):
            for x in range(W):
                cell = maze.grid.get_cell(x, y)
                _y, _x = y * 2 + 1, x * 2 + 1
                grid[_y][_x] = " "

                if cell.walls["N"]:
                    grid[_y - 1][_x] = " "
                if cell.walls["S"]:
                    grid[_y + 1][_x] = " "
                if cell.walls["E"]:
                    grid[_y][_x + 1] = " "
                if cell.walls["W"]:
                    grid[_y][_x - 1] = " "

        result = ""
        for row in grid:
            result += "".join(row) + "\n"

        return result

    def display_grid(self, maze: MazeGenerator) -> None:
        self.center_text(self._create_grid(maze))


def display(stdscr: Win, maze: MazeGenerator) -> None:
    curses.curs_set(0)
    disp = Display(stdscr)
    disp.stdscr.clear()
    disp.display_grid(maze)
    disp.stdscr.getch()