from validate_config import validate
from Errors import InvalidEntryError, InvalidFileError, InvalidArgumentError

import sys
import os

def main() -> None:

    try:
        if len(sys.argv) != 2:
            raise InvalidArgumentError("Please provide configuration file as argument. Usage: python3 a_maze_ing.py config.txt")

        filename = sys.argv[1]
        _, extension = os.path.splitext(filename)

        if extension != '.txt':
            raise InvalidFileError("Configuration file must be plain text (eg: config.txt)")
        
        valid_data = validate(filename)

        print(valid_data)
    except InvalidEntryError as e:
        print(f"ERROR: {e}")
    except InvalidArgumentError as e:
        print(f"ERROR: {e}")
    except InvalidFileError as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
