from typing import Dict, List, Any
from Errors import InvalidConfigError

import sys


def valid_key(key: str) -> bool:
    """
    Check for key is valid and exists in required keys.

    args:
        key (str): extracted key from config file.

    returns:
        bool: True if the key is valid. False if not.
    """

    required_keys: List[str] = [
            'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    optional_keys: List[str] = ['SEED', 'ALGORITHM']

    if key in required_keys or key in optional_keys:
        return True
    return False


def extract_item(item: List[str]) -> Dict[str, Any]:
    """
    Validate item individually & convert valid data to dict.

    args:
        item (List[str]): string split by '='

    returns:
        Dict: contain status and data in case of success.
              If validation fails dict contain status and error.
    """

    result: Dict[str, Any] = {}

    if len(item) == 2:
        k, v = item
        result[k.strip(' "')] = v.strip(' "')
    elif len(item) == 1:
        k = item[0]
        result[k] = ""
    else:
        return {
            "status": "fail",
            "error": f"'{item[0]}' not valid. Item should follow this pattern KEY=VALUE."
        }
    return {"status": "success", "data": result}



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

                # Check for data is valid.
                data: Dict[str, Any] = extract_item(item)
                if data['status'] == 'fail':
                    raise InvalidConfigError(data['error'])

                # Check is key is valid
                key = list(data['data'].keys())[-1]
                val = data['data'][key] if data['data'][key] else ""
                if not valid_key(key):
                    raise InvalidConfigError(
                            f"'{key}': Invalid configuration key.")

                # Convert data to dictionary
                config[key] = val

        return config

    except InvalidConfigError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"ERROR: '{path}' configuration file not exist.")
        sys.exit(1)
    except OSError as e:
        print(f"ERROR: Something wrong! {e}")
        sys.exit(1)
