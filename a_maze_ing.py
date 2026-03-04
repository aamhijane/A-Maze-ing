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

        # If SEED exist
        if seed != None:
            random.seed(seed)

        cell_a = mazegen.Cell(0, 0)

        cell_a.walls["N"] = True
        cell_a.walls["E"] = True
        cell_a.walls["S"] = True

        print(cell_a.to_hex())

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
