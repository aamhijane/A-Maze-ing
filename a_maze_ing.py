from config_parser import parse_config
from maze_engine import MazeGrid

def main() -> None:
    data = parse_config("default.cfg")
    width = data['data']['WIDTH']
    height = data['data']['HEIGHT']
    entry = data['data']['ENTRY']

    maze = MazeGrid(width, height)

    maze.generate(entry)

    maze.display_raw()

if __name__ == "__main__":
    main()
