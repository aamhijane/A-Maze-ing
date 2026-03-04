from typing import Dict, List, Any
from Errors import InvalidEntryError

import sys


def config_parsing(path: str) -> Dict[str, Any]:
    """
    Parse config file data & error handling.

    args:
        path (str): configuration file path.

    returns:
        dict: filtered and parsed configuration data.
    """

    try:
        with open(path, "r") as file:
            config: Dict[str, Any] = {}

            for line in file:
                clean_line: str = line.strip()

                # Skip comment & empty line
                if not clean_line or clean_line.startswith("#"):
                    continue

                # Extract data by spliting it.
                item: List[str] = clean_line.split('=')
                if len(item) != 2 or item[1] == '':
                    raise InvalidEntryError(
                            f"This entry '{item[0]}' cannot be empty.")

                k, v = item

                # Convert data to dictionary
                config[k] = v

        return config

    except FileNotFoundError:
        print(f"ERROR: '{path}' configuration file not exist.")
        sys.exit(1)
    except OSError as e:
        print(f"ERROR: Something wrong! {e}")
        sys.exit(1)
