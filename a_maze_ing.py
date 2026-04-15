from typing import Dict, Any
from validate_config import validate
from display import display
from mazegen.errors import (
    InvalidEntryError,
    InvalidFileError,
    InvalidArgumentError,
    InvalidConfigError,
    MazeSizeError

)
from mazegen import MazeGenerator, MazeWriter
import curses
import sys
import os


def main() -> None:
    """Entry point for the maze generator program.

    Reads the configuration file path from command-line arguments,
    validates it, generates a maze, and prints the solution path.

    Raises:
        InvalidArgumentError: If the wrong number of arguments is provided.
        InvalidFileError: If the config file has an invalid extension.
        InvalidEntryError: If the config file contains invalid entries.
    """
    try:
        if len(sys.argv) != 2:
            raise InvalidArgumentError(
                "Usage: python3 a_maze_ing.py config.txt"
            )

        filename: str = sys.argv[1]
        _, extension = os.path.splitext(filename)

        if extension != ".txt":
            raise InvalidFileError(
                "Configuration file must be plain text (e.g. config.txt)."
            )

        config: Dict[str, Any] = validate(filename)

        maze = MazeGenerator(
            width=config['WIDTH'],
            height=config['HEIGHT'],
            seed=config['SEED'],
            perfect=config['PERFECT'],
            entry_point=config['ENTRY'],
            exit_point=config['EXIT']
        )

        path: str = maze.solve()
        if not path:
            raise InvalidConfigError(
                "No solution found for this maze. "
                "ENTRY/EXIT must be out of 42 pattern.")

        maze_writer = MazeWriter(maze, config["OUTPUT_FILE"])
        maze_writer.write()
        curses.wrapper(display, maze)

    except (
            InvalidEntryError,
            InvalidFileError,
            InvalidArgumentError,
            InvalidConfigError,
            MazeSizeError
    ) as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Exiting (sig quit)...")


if __name__ == "__main__":
    main()
