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

        # Check if width or height values can't be converted to int.
        # Check if width or height values is less or equal 0.
        if k == 'WIDTH' or k == 'HEIGHT':

            if not convert_to_int(v):
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': Should be a number."
                }

            config[k] = int(v)

            if config[k] <= 0:
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': Should be larger than 0."
                }

        # Check if entry or exit values can't be converted to int.
        # Check if entry or exit values is out of bounds.
        # Check if entry or exit values are equal.
        if k == 'ENTRY' or k == 'EXIT':
            coords = data[k].split(',')
            if not coords or len(coords) != 2:
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': Should have valid (x,y) coordinates."
                }

            x, y = coords
            if not convert_to_int(x) or not convert_to_int(y):
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': (x,y) coordinates should be numbers."
                }

            config[k] = (int(x), int(y))

            valid_x = (0 <= config[k][0] < config['WIDTH']) 
            valid_y = (0 <= config[k][1] < config['HEIGHT']) 
            if not valid_x or not valid_y:
                return {
                    "status": "fail",
                    "error": f"Invalid '{k}': (x,y) coordinates out of bounds."
                }
    
    return {"status": "success", "data": config}
