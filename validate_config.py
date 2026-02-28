from typing import Dict, List, Any
from parse_config import config_parsing

import os


def convert_to_int(val: str) -> bool:
    try:
        int(val)
        return True
    except ValueError:
        return False


def validate(path: str) -> Dict[str, Any]:
    
    config: Dict[str, Any] = {}
    data: Dict[str, str] = config_parsing(path)
    
    # CONFIG KEYS
    config_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']

    # Check if all required keys exist.
    for k in config_keys:
        if k not in data:
            raise InvalidEntryError(
                f"Required configuration entry '{k}' is missing.")


    # Validate data
    for k, v in data.items():

        # Validate width & height.
        if k == 'WIDTH' or k == 'HEIGHT':

            # Check if width or height values can't be converted to int.
            if not convert_to_int(v):
                raise InvalidEntryError(f"Invalid number. Letters and special characters are not allowed for this entry '{k}'.")

            config[k] = int(v)

            # Check if width or height values is less or equal 0.
            if config[k] <= 0:
                raise InvalidEntryError(f"'{k}' value must be 1 or higher.")

        # Validate entry & exit.
        elif k == 'ENTRY' or k == 'EXIT':
            coords = data[k].split(',')

            # Check if coords not exists or invalid
            if not coords or len(coords) != 2:
                raise InvalidEntryError(f"Invalid '{k}': Should have valid (x,y) coordinates.")

            x, y = coords

            # Check if entry or exit values can't be converted to int.
            if not convert_to_int(x) or not convert_to_int(y):
                raise InvalidEntryError(f"'{k}' x,y coordinates should not be empty.")

            # Store coordinates
            config[k] = (int(x), int(y))

            valid_x = (0 <= config[k][0] < config['WIDTH']) 
            valid_y = (0 <= config[k][1] < config['HEIGHT']) 

            # Check if entry or exit values is out of bounds.
            if not valid_x or not valid_y:
                raise InvalidEntryError(f"'{k}' x,y coordinates are out of bounds.")

        # Validate perfect
        elif k == 'PERFECT':
            perfect: str = data[k].lower()

            # Check if empty or value not true or false.
            if not perfect or (perfect != 'true' and perfect != 'false'):
                raise InvalidEntryError(f"'{k}' entry should be 'True' or 'False'.")

            value: bool = True if perfect == 'true' else False
            config[k] = value


        # Validate output file.
        elif k == 'OUTPUT_FILE':
            if not data[k]:
                raise InvalidEntryError(
                        f"'{k}' entry should not be empty. Provide an output file (eg: maze.txt).")

            _, ext = os.path.splitext(data[k])
            if ext != '.txt':
                raise InvalidFileError("The output file must be a plain text (eg: maze.txt)")

        # Validate seed.
        elif k == 'SEED':

            if not v:
                continue

            # Check if seed value can't be converted to int.
            if not convert_to_int(v):
                raise InvalidEntryError(f"'{k}' entry must be a positive number.")

            config[k] = int(v)

            # Check if seed value is less or equal 0.
            if config[k] <= 0:
                raise InvalidEntryError(f"'{k}' entry must be 1 or higher.")


        # Validate algorithm
        elif k == 'ALGORITHM':
            algorithms: List[str] = ['recursive_backtracker', 'prim', 'kruskal', 'eller']

            if not v:
                continue

            # Check if algorithm not valid
            if v and v in algorithms:
                config[k] = data[k]
            else:
                raise InvalidEntryError(
                        f"'{k}' entry should be one these: '\n- recursive_backtracker\n- prim\n- kruskal\n- eller'.")

        else:
            raise InvalidEntryError(
                    f"Configuration file has invalid key: '{k}'")


    # Check if entry or exit values are equal.
    if config['ENTRY'] == config['EXIT']:
        raise InvalidEntryError(f"The starting(ENTRY) and ending(EXIT) points must be different.")

    if 'SEED' not in config.keys():
        config['SEED'] = None

    if 'ALGORITHM' not in config.keys():
        config['ALGORITHM'] = 'recursive_backtracker'
    
    return config
