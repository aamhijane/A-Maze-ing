from typing import Dict, Any, Optional


def parse_config(file_path: str) -> Dict[str, Any]:
    REQUIRED_KEYS: Dict = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE"}
    raw_data: Dict = {}

    try:
        with open(file_path, "r") as file:
            for line in file:
                # 1. Clean and Filter
                line = line.split('#')[0].strip() # Handles inline comments
                if not line or '=' not in line:
                    continue

                # 2. Strict Key Extraction
                key, value = [part.strip().strip('"') for part in line.split('=', 1)]
                if key in REQUIRED_KEYS:
                    raw_data[key] = value

        # 3. Verify all keys were found
        missing = REQUIRED_KEYS - set(raw_data.keys())
        if missing:
            return {"status": "failed", "error_msg": f"Missing keys: {', '.join(missing)}"}

        # 4. Deep Validation (The Hardened Way)
        config = {}
        try:
            config['WIDTH'] = int(raw_data['WIDTH'])
            config['HEIGHT'] = int(raw_data['HEIGHT'])
            
            if config['WIDTH'] <= 0 or config['HEIGHT'] <= 0:
                raise ValueError("Dimensions must be positive.")

            # Coordinate parsing
            for k in ['ENTRY', 'EXIT']:
                parts = raw_data[k].split(',')
                if len(parts) != 2:
                    raise ValueError(f"Invalid format for {k}. Expected x,y")
                coords = (int(parts[0]), int(parts[1]))
                
                # Boundary Checks
                if not (0 <= coords[0] < config['WIDTH'] and 0 <= coords[1] < config['HEIGHT']):
                    raise ValueError(f"{k} {coords} is out of maze boundaries.")
                config[k] = coords

            config['OUTPUT_FILE'] = raw_data['OUTPUT_FILE']

        except ValueError as e:
            return {"status": "failed", "error_msg": str(e)}

        if config['ENTRY'] == config['EXIT']:
            return {"status": "failed", "error_msg": "ENTRY and EXIT cannot be the same."}

        return {"status": "success", "data": config}

    except FileNotFoundError:
        return {"status": "failed", "error_msg": f"File '{file_path}' not found."}
