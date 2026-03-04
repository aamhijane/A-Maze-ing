from typing import Dict, Any
from validate_config import validate
from Errors import InvalidEntryError, InvalidFileError, InvalidArgumentError

import sys
import os
import random
import mazegen


def main() -> None:

    try:
        if len(sys.argv) != 2:
            raise InvalidArgumentError(
                "Please provide configuration file as argument. Usage: python3 a_maze_ing.py config.txt"
            )

        filename = sys.argv[1]
        _, extension = os.path.splitext(filename)

        if extension != ".txt":
            raise InvalidFileError(
                "Configuration file must be plain text (eg: config.txt)"
            )

        valid_data: Dict[str, Any] = validate(filename)

        seed: Any = valid_data["SEED"]
        width: int = valid_data["WIDTH"]
        height: int = valid_data["HEIGHT"]

        # If SEED exist
        if seed != None:
            random.seed(seed)

        grid = mazegen.Grid(width, height)

        print(grid.cells[-1][-1].walls)
        print(grid.cells[-1][-1].walls)

    except InvalidEntryError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except InvalidArgumentError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except InvalidFileError as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
