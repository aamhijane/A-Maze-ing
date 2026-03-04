from typing import Dict, List
from Errors import InvalidEntryError, InvalidFileError

import sys


def config_parsing(path: str) -> Dict[str, str]:
    """
    Parse config file data & error handling.

    args:
        path (str): configuration file path.

    returns:
        dict: filtered and parsed configuration data.
    """

    try:
        with open(path, "r") as file:
            config: Dict[str, str] = {}

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
        raise InvalidFileError(f"'{path}' configuration file not exist.")
    except OSError as e:
        raise InvalidFileError(f"Unexpected file error: {e}")
