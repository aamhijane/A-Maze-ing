from typing import Dict, Any
from parse_config import config_parsing


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
            return {
                "status": "fail",
                "error": f"'{k}': Missing or invalid key."
            }


    # Validate data
    for k, v in data.items():

        # Validate width & height.
        if k == 'WIDTH' or k == 'HEIGHT':

            # Check if width or height values can't be converted to int.
            if not convert_to_int(v):
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': Should be a number."
                }

            config[k] = int(v)

            # Check if width or height values is less or equal 0.
            if config[k] <= 0:
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': Should be larger than 0."
                }

        # Validate entry & exit.
        if k == 'ENTRY' or k == 'EXIT':
            coords = data[k].split(',')

            # Check if coords not exists or invalid
            if not coords or len(coords) != 2:
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': Should have valid (x,y) coordinates."
                }

            x, y = coords

            # Check if entry or exit values can't be converted to int.
            if not convert_to_int(x) or not convert_to_int(y):
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': (x,y) coordinates should be numbers."
                }

            # Store coordinates
            config[k] = (int(x), int(y))

            valid_x = (0 <= config[k][0] < config['WIDTH']) 
            valid_y = (0 <= config[k][1] < config['HEIGHT']) 

            # Check if entry or exit values is out of bounds.
            if not valid_x or not valid_y:
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': (x,y) coordinates out of bounds."
                }

        # Validate perfect
        if k == 'PERFECT':
            perfect: str = data[k].lower()

            # Check if empty or value not true or false.
            if not perfect or (perfect != 'true' and perfect != 'false'):
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': Should be 'True' or 'False'."
                }

            value: bool = True if perfect == 'true' else False
            config[k] = value


        # Validate output file.
        if k == 'OUTPUT_FILE':
            if not data[k]:
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': Coudn't be empty. Provide an output file (eg: maze.txt)."
                }

        # Validate seed.
        if k == 'SEED':

            if not v:
                continue

            # Check if seed value can't be converted to int.
            if not convert_to_int(v):
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': Should be a number."
                }

            config[k] = int(v)

            # Check if seed value is less or equal 0.
            if config[k] <= 0:
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': Should be larger than 0."
                }


        # Validate algorithm
        algorithms: List[str] = ['recursive_backtracker', 'prim', 'kruskal', 'eller']

        if k == 'ALGORITHM':
            if not v:
                continue

            # Check if algorithm not valid
            if v and v in algorithms:
                config[k] = data[k]
            else:
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': Shoud be one these: 'recursive_backtracker', 'prim', 'kruskal', 'eller'."
                }


    # Check if entry or exit values are equal.
    if config['ENTRY'] == config['EXIT']:
        return {
            "status": "fail",
            "error": f"ENTRY & EXIT coordinates should be not equals."
        }

    if 'SEED' not in config.keys():
        config['SEED'] = None

    if 'ALGORITHM' not in config.keys():
        print("DEBUG")
        config['ALGORITHM'] = 'recursive_backtracker'
    
    return {"status": "success", "data": config}
