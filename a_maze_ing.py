from typing import Dict, Any
from validate_config import validate
from mazegen.errors import (
    InvalidEntryError,
    InvalidFileError,
    InvalidArgumentError,
)
from mazegen import MazeGenerator, MazeWriter

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
            print("WARNING: No solution found for this maze.")

        print("SEED", maze.get_seed())


        maze_writer = MazeWriter(maze, config["OUTPUT_FILE"])
        maze_writer.write()

    except (
            InvalidEntryError,
            InvalidFileError,
            InvalidArgumentError,
    ) as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
