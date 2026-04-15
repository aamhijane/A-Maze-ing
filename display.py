"""Curses-based interactive display for the A-Maze-ing maze generator.

Renders a maze in the terminal using block characters, animates its
construction, shows the solution path, and handles keyboard input for
regeneration, theming, speed and animation-style changes.
"""

import curses
import random
import time
from typing import List, Tuple

from mazegen import MazeGenerator, MazeWriter

Win = curses.window

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PATTERN_42: List[List[int]] = [
    [1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]

THEMES: List[Tuple[int, ...]] = [
    (curses.COLOR_WHITE, curses.COLOR_BLACK,
     curses.COLOR_RED, curses.COLOR_BLACK,
     curses.COLOR_BLACK, curses.COLOR_GREEN,
     curses.COLOR_BLACK, curses.COLOR_YELLOW),
    (curses.COLOR_CYAN, curses.COLOR_BLACK,
     curses.COLOR_MAGENTA, curses.COLOR_BLACK,
     curses.COLOR_BLACK, curses.COLOR_GREEN,
     curses.COLOR_BLACK, curses.COLOR_YELLOW),
    (curses.COLOR_BLUE, curses.COLOR_BLACK,
     curses.COLOR_YELLOW, curses.COLOR_BLACK,
     curses.COLOR_BLACK, curses.COLOR_GREEN,
     curses.COLOR_BLACK, curses.COLOR_RED),
    (curses.COLOR_YELLOW, curses.COLOR_BLACK,
     curses.COLOR_CYAN, curses.COLOR_BLACK,
     curses.COLOR_BLACK, curses.COLOR_GREEN,
     curses.COLOR_BLACK, curses.COLOR_MAGENTA),
    (curses.COLOR_GREEN, curses.COLOR_BLACK,
     curses.COLOR_RED, curses.COLOR_BLACK,
     curses.COLOR_BLACK, curses.COLOR_CYAN,
     curses.COLOR_BLACK, curses.COLOR_YELLOW),
    (curses.COLOR_MAGENTA, curses.COLOR_BLACK,
     curses.COLOR_GREEN, curses.COLOR_BLACK,
     curses.COLOR_BLACK, curses.COLOR_CYAN,
     curses.COLOR_BLACK, curses.COLOR_YELLOW),
]

THEME_NAMES: List[str] = [
    "White", "Cyan", "Blue", "Yellow", "Green", "Magenta"
]
SPEEDS: List[float] = [0.10, 0.04, 0.02, 0.005, 0.0]
SPEED_LABELS: List[str] = ["Slow", "Normal", "Fast", "Turbo", "Instant"]

# ---------------------------------------------------------------------------
# Module-level state
# ---------------------------------------------------------------------------

symbols_index: int = 0
animation: int = 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_gaps(stdscr: Win, maze: MazeGenerator) -> Tuple[int, int]:
    """Return (y_gap, x_gap) to centre the maze in the current terminal."""
    h, w = stdscr.getmaxyx()
    maze_width = maze.width * 4 + 1
    maze_height = maze.height * 2 + 1
    return (
        max(0, (h - maze_height) // 2),
        max(0, (w - maze_width) // 2),
    )


def color_outer_wall(stdscr: Win, maze: MazeGenerator) -> None:
    """Draw a decorative border around the maze using block characters."""
    y_gap, x_gap = get_gaps(stdscr, maze)

    for y in range(maze.height * 2 + 1):
        stdscr.addstr(
            y + y_gap,
            0 + x_gap,
            "█ ",
            curses.color_pair(6),
        )
        stdscr.addstr(
            y + y_gap,
            maze.width * 4 + x_gap,
            " █",
            curses.color_pair(6),
        )

    for x in range(maze.width * 4 - 3):
        stdscr.addstr(
            0 + y_gap,
            x + 2 + x_gap,
            "▀▀▀▀",
            curses.color_pair(6),
        )
        stdscr.addstr(
            maze.height * 2 + y_gap,
            x + 2 + x_gap,
            "▄▄▄▄",
            curses.color_pair(6),
        )

    stdscr.addstr(
        maze.height * 2 + y_gap,
        maze.width * 4 + x_gap,
        "█",
        curses.color_pair(6) | curses.A_REVERSE,
    )
    stdscr.addstr(
        0 + y_gap,
        maze.width * 4 + x_gap,
        "█",
        curses.color_pair(6) | curses.A_REVERSE,
    )
    stdscr.addstr(
        0 + y_gap,
        0 + x_gap,
        "▄",
        curses.color_pair(6) | curses.A_REVERSE,
    )
    stdscr.addstr(
        maze.height * 2 + y_gap,
        0 + x_gap,
        "▀",
        curses.color_pair(6) | curses.A_REVERSE,
    )


def apply_theme(theme_idx: int) -> None:
    """Initialise curses colour pairs for the given theme index."""
    t = THEMES[theme_idx % len(THEMES)]
    curses.init_pair(1, t[0], t[1])
    curses.init_pair(4, t[2], t[3])
    curses.init_pair(5, t[4], t[5])
    curses.init_pair(6, t[6], t[7])


def get_path_cells(maze: MazeGenerator) -> List[Tuple[int, int]]:
    """Return an ordered list of (x, y) grid cells along the solution path."""
    cx, cy = maze.entry_point
    cells: List[Tuple[int, int]] = [(cx, cy)]
    for d in maze.solve():
        if d == "N":
            cy -= 1
        elif d == "S":
            cy += 1
        elif d == "E":
            cx += 1
        elif d == "W":
            cx -= 1
        cells.append((cx, cy))
    return cells


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

def draw_grid(stdscr: Win, maze: MazeGenerator) -> None:
    """Render the fully-built maze grid (open passages and walls)."""
    y_gap, x_gap = get_gaps(stdscr, maze)

    grid = [
        ["██"] * (maze.width * 2 + 1)
        for _ in range(maze.height * 2 + 1)
    ]

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid.get_cell(x, y)
            gy, gx = y * 2 + 1, x * 2 + 1
            grid[gy][gx] = "  "
            if cell.walls["N"]:
                grid[gy - 1][gx] = "  "
            if cell.walls["S"]:
                grid[gy + 1][gx] = "  "
            if cell.walls["E"]:
                grid[gy][gx + 1] = "  "
            if cell.walls["W"]:
                grid[gy][gx - 1] = "  "

    for row_i, row in enumerate(grid):
        for col_i, tile in enumerate("".join(row)):
            stdscr.addstr(
                row_i + y_gap, col_i + x_gap, tile, curses.color_pair(1)
            )


def draw_path(
    stdscr: Win,
    maze: MazeGenerator,
    cells: List[Tuple[int, int]],
    step: int,
    animating: bool,
) -> None:
    """Draw the solution path, optionally clipped to *step* cells.

    Args:
        stdscr:    The curses window to draw into.
        maze:      The current maze instance (used for coordinate offsets).
        cells:     Ordered list of (x, y) solution cells.
        step:      How many cells to reveal when *animating* is True.
        animating: When True only cells up to *step* are rendered.
    """
    y_gap, x_gap = get_gaps(stdscr, maze)

    limit = step if animating else len(cells)
    symbols = ["🔶", "🔷", "🍀"]

    for cx, cy in cells[:limit]:
        stdscr.addstr(
            cy * 2 + 1 + y_gap,
            cx * 4 + 2 + x_gap,
            symbols[symbols_index],
            curses.color_pair(4),
        )
    draw_markers(stdscr, maze)


def draw_markers(stdscr: Win, maze: MazeGenerator) -> None:
    """Draw the entry (🐇), exit (🥕) and optional '42' pattern markers."""
    y_gap, x_gap = get_gaps(stdscr, maze)

    ex, ey = maze.entry_point
    xx, xy = maze.exit_point

    stdscr.addstr(
        ey * 2 + 1 + y_gap, ex * 4 + 2 + x_gap, "🐇", curses.color_pair(1)
    )
    stdscr.addstr(
        xy * 2 + 1 + y_gap, xx * 4 + 2 + x_gap, "🥕", curses.color_pair(1)
    )

    if maze.is_small:
        return

    for ri, row in enumerate(PATTERN_42):
        for ci, v in enumerate(row):
            if v:
                stdscr.addstr(
                    (maze.start_y + ri) * 2 + 1 + y_gap,
                    (maze.start_x + ci) * 4 + 2 + x_gap,
                    "  ",
                    curses.color_pair(6),
                )


def draw_walls(stdscr: Win, maze: MazeGenerator) -> None:
    """Fill the screen with solid wall tiles (used at animation start)."""
    y_gap, x_gap = get_gaps(stdscr, maze)

    for gy in range(maze.height * 2 + 1):
        for gx in range(maze.width * 2 + 1):
            if gy % 2 == 0 or gx % 2 == 0:
                stdscr.addstr(
                    gy + y_gap, gx * 2 + x_gap, "██", curses.color_pair(1)
                )
    color_outer_wall(stdscr, maze)


# ---------------------------------------------------------------------------
# Animation order generators
# ---------------------------------------------------------------------------

def random_animation(maze: MazeGenerator) -> List[Tuple[int, int]]:
    """Return all maze cells in a random order for the reveal animation."""
    coords: List[Tuple[int, int]] = []
    for y in range(maze.height):
        for x in range(maze.width):
            coords.append((x, y))
    random.shuffle(coords)
    return coords


def line_by_line_animation(maze: MazeGenerator) -> List[Tuple[int, int]]:
    """Return all maze cells ordered top-to-bottom, left-to-right."""
    coords: List[Tuple[int, int]] = []
    for y in range(maze.height):
        for x in range(maze.width):
            coords.append((x, y))
    return coords


def butterfly_animation(maze: MazeGenerator) -> List[Tuple[int, int]]:
    """Return cells in a mirrored pattern that expands from corners inward."""
    coords: List[Tuple[int, int]] = []
    for y in range(maze.height):
        for x in range(maze.width):
            coords.append((x, y))
            coords.append((maze.width - 1 - x, maze.height - 1 - y))
    return coords


animations: list = [
    random_animation, line_by_line_animation, butterfly_animation
]


def build_steps(maze: MazeGenerator) -> List[List[Tuple[int, int]]]:
    """Build the per-frame reveal sequence for the maze construction animation.

    Each element is a list of (row, col) grid positions that should be
    cleared (turned from wall to open) in that animation tick.

    Args:
        maze: The maze whose cells are converted into animation steps.

    Returns:
        A list of steps; each step is a list of (gy, gx) coordinates.
    """
    steps: List[List[Tuple[int, int]]] = []
    coords = animations[animation](maze)

    for x, y in coords:
        cell = maze.grid.get_cell(x, y)

        real_x = (x * 2) + 1
        real_y = (y * 2) + 1

        actions: List[Tuple[int, int]] = [(real_y, real_x)]

        if cell.walls["N"]:
            actions.append((real_y - 1, real_x))
        if cell.walls["S"]:
            actions.append((real_y + 1, real_x))
        if cell.walls["W"]:
            actions.append((real_y, real_x - 1))
        if cell.walls["E"]:
            actions.append((real_y, real_x + 1))
        steps.append(actions)
    return steps


# ---------------------------------------------------------------------------
# UI chrome
# ---------------------------------------------------------------------------

def draw_menu(
    stdscr: Win, maze: MazeGenerator, theme_idx: int, speed_idx: int
) -> None:
    """Render the interactive key-binding menu below the maze.

    Args:
        stdscr:    The curses window.
        maze:      Used to position the menu beneath the maze.
        theme_idx: Index into THEMES / THEME_NAMES for the current theme.
        speed_idx: Index into SPEEDS / SPEED_LABELS for the current speed.
    """
    y_gap, x_gap = get_gaps(stdscr, maze)

    y = maze.height * 2 + 2 + y_gap
    theme = THEME_NAMES[theme_idx % len(THEME_NAMES)]
    speed = SPEED_LABELS[speed_idx]
    stdscr.addstr(y, 0 + x_gap, "=== A-Maze-ing ===".ljust(50))
    stdscr.addstr(y + 1, 0 + x_gap, "1. Re-generate maze".ljust(50))
    stdscr.addstr(y + 2, 0 + x_gap, "2. Show/Hide solution path".ljust(50))
    stdscr.addstr(
        y + 3, 0 + x_gap, f"3. Rotate colors  [theme: {theme}]".ljust(50)
    )
    stdscr.addstr(
        y + 4, 0 + x_gap, f"4. Animation speed  [{speed}]".ljust(50)
    )
    stdscr.addstr(
        y + 5, 0 + x_gap,
        f"5. perfect/imperfect  [{maze.perfect}]".ljust(50)
    )
    stdscr.addstr(y + 7, 0 + x_gap, "7. Change path symbols".ljust(50))
    stdscr.addstr(
        y + 8,
        0 + x_gap,
        f"8. Change animation [{animations[animation].__name__}]".ljust(50),
    )
    stdscr.addstr(y + 6, 0 + x_gap, "6. Quit".ljust(50))
    stdscr.addstr(y + 9, 0 + x_gap, "Choice? (1-6)".ljust(50))
    if maze.is_small:
        stdscr.addstr(
            y + 10, 0 + x_gap,
            "Note: Maze is too small to embed the '42' pattern.".ljust(50)
        )


# ---------------------------------------------------------------------------
# Terminal-size guards
# ---------------------------------------------------------------------------

def check_terminal_size(stdscr: Win, maze: MazeGenerator) -> bool:
    """Return True if the terminal is large enough to display the maze.

    Calls :func:`show_resize_error` and returns False when it is not.
    """
    h, w = stdscr.getmaxyx()
    maze_width = maze.width * 4 + 1
    maze_height = maze.height * 2 + 1
    if h < maze_height + 10 or w < maze_width + 2:
        show_resize_error(stdscr)
        return False
    return True


def show_resize_error(stdscr: Win) -> None:
    """Display a terminal-too-small error message and wait briefly."""
    stdscr.clear()
    try:
        stdscr.addstr(
            0, 0,
            "Terminal too small for the maze. Please resize and try again.",
        )
    except curses.error:
        pass
    stdscr.refresh()
    curses.napms(200)


# ---------------------------------------------------------------------------
# Full scene redraw
# ---------------------------------------------------------------------------

def redraw_scene(
    stdscr: Win,
    maze: MazeGenerator,
    theme_idx: int,
    speed_idx: int,
    maze_anim: bool,
    show_path: bool,
    path_cells: List[Tuple[int, int]],
    path_step: int,
    path_anim: bool,
) -> None:
    """Clear and redraw the entire scene (maze, path, menu).

    Args:
        stdscr:     The curses window.
        maze:       The current maze instance.
        theme_idx:  Active colour-theme index.
        speed_idx:  Active animation-speed index.
        maze_anim:  True while the maze build animation is running.
        show_path:  True when the solution path should be visible.
        path_cells: Ordered solution cells.
        path_step:  Current animation frame for path reveal.
        path_anim:  True while the path reveal animation is running.
    """
    stdscr.clear()
    if maze_anim:
        draw_walls(stdscr, maze)
    else:
        draw_grid(stdscr, maze)
        color_outer_wall(stdscr, maze)
        draw_markers(stdscr, maze)
    if show_path:
        draw_path(stdscr, maze, path_cells, path_step, path_anim)
    draw_menu(stdscr, maze, theme_idx, speed_idx)
    stdscr.refresh()


# ---------------------------------------------------------------------------
# Main event loop
# ---------------------------------------------------------------------------

def display(stdscr: Win, maze: MazeGenerator) -> None:
    """Run the interactive curses event loop for the maze display.

    Handles:
    - Animated maze construction (key 1 re-generates).
    - Animated solution path reveal (key 2 toggles).
    - Colour-theme cycling (key 3).
    - Animation speed cycling (key 4).
    - Perfect / imperfect maze toggle (key 5).
    - Path-symbol cycling (key 7, only while path is shown).
    - Animation-style cycling (key 8).
    - Graceful terminal-resize handling.
    - Quit on key 6 or 'q'.

    Args:
        stdscr: The curses window provided by :func:`curses.wrapper`.
        maze:   The initial :class:`~mazegen.MazeGenerator` instance.
    """
    curses.start_color()
    curses.curs_set(0)
    stdscr.nodelay(True)

    theme_idx = 0
    speed_idx = 3
    apply_theme(theme_idx)

    steps = build_steps(maze)
    step = 0
    maze_anim = True

    path_cells: List[Tuple[int, int]] = []
    path_step = 0
    path_anim = False
    show_path = False
    error_mode = False

    last_tick = time.time()
    try:
        redraw_scene(
            stdscr,
            maze,
            theme_idx,
            speed_idx,
            maze_anim,
            show_path,
            path_cells,
            path_step,
            path_anim,
        )
    except curses.error:
        error_mode = True
        show_resize_error(stdscr)

    while True:
        try:
            if error_mode:
                key = stdscr.getch()
                if key == ord('6') or key == ord('q'):
                    break
                if (
                    key == curses.KEY_RESIZE
                    or check_terminal_size(stdscr, maze)
                ):
                    error_mode = False
                    redraw_scene(
                        stdscr,
                        maze,
                        theme_idx,
                        speed_idx,
                        maze_anim,
                        show_path,
                        path_cells,
                        path_step,
                        path_anim,
                    )
                else:
                    show_resize_error(stdscr)
                continue

            delay = SPEEDS[speed_idx]
            now = time.time()
            ticked = delay == 0.0 or (now - last_tick >= delay)

            # maze build animation
            if maze_anim and ticked:
                batch = steps[step:] if delay == 0.0 else [steps[step]]
                y_gap, x_gap = get_gaps(stdscr, maze)
                for coords in batch:
                    for ry, rx in coords:
                        stdscr.addstr(
                            ry + y_gap,
                            rx * 2 + x_gap,
                            "  ",
                            curses.color_pair(1),
                        )
                step += len(batch)
                if step >= len(steps):
                    maze_anim = False
                    draw_markers(stdscr, maze)
                last_tick = now
                stdscr.refresh()
            # path animation
            elif show_path and path_anim and ticked:
                path_step = (
                    len(path_cells) if delay == 0.0 else path_step + 1
                )
                if path_step >= len(path_cells):
                    path_anim = False
                draw_path(stdscr, maze, path_cells, path_step, path_anim)
                last_tick = now
                stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_RESIZE:
                if not check_terminal_size(stdscr, maze):
                    continue
                stdscr.clear()
                if maze_anim:
                    draw_walls(stdscr, maze)
                else:
                    draw_grid(stdscr, maze)
                    color_outer_wall(stdscr, maze)
                    draw_markers(stdscr, maze)
                if show_path:
                    draw_path(stdscr, maze, path_cells, path_step, path_anim)
                draw_menu(stdscr, maze, theme_idx, speed_idx)
                stdscr.refresh()
                continue

            if key == -1:
                continue

            if key == ord('1') and not maze_anim:
                maze = MazeGenerator(
                    maze.width, maze.height, maze.seed,
                    maze.perfect, maze.entry_point, maze.exit_point,
                )
                MazeWriter(maze, "maze.txt").write()
                steps = build_steps(maze)
                step = 0
                maze_anim = True
                show_path = False
                stdscr.erase()
                draw_walls(stdscr, maze)

            elif key == ord('2') and not maze_anim:
                show_path = not show_path
                if show_path:
                    path_cells = get_path_cells(maze)
                    path_step = 0
                    path_anim = True
                else:
                    path_anim = False
                    stdscr.erase()
                    draw_grid(stdscr, maze)
                    color_outer_wall(stdscr, maze)
                    draw_markers(stdscr, maze)

            elif key == ord('3'):
                theme_idx += 1
                apply_theme(theme_idx)
                if not maze_anim:
                    draw_grid(stdscr, maze)
                    draw_markers(stdscr, maze)
                    color_outer_wall(stdscr, maze)
                    if show_path:
                        draw_path(
                            stdscr, maze, path_cells, path_step, path_anim
                        )

            elif key == ord('4'):
                speed_idx = (speed_idx + 1) % len(SPEEDS)

            elif key == ord('5') and not maze_anim:
                maze = MazeGenerator(
                    maze.width, maze.height, maze.seed,
                    not maze.perfect, maze.entry_point, maze.exit_point,
                )
                MazeWriter(maze, "maze.txt").write()
                steps = build_steps(maze)
                step = 0
                maze_anim = True
                show_path = False
                stdscr.erase()
                draw_walls(stdscr, maze)

            elif key == ord('6') or key == ord('q'):
                break
            elif key == ord('7') and show_path:
                global symbols_index
                symbols_index = (symbols_index + 1) % 3
                draw_path(stdscr, maze, path_cells, path_step, path_anim)
            elif key == ord('8'):
                global animation
                animation = (animation + 1) % 3

            draw_menu(stdscr, maze, theme_idx, speed_idx)
            stdscr.refresh()
        except curses.error:
            if error_mode:
                continue
            error_mode = True
            show_resize_error(stdscr)
            continue
