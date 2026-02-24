from config_parser import parse_config
from maze_engine import MazeGrid

def main() -> None:
    data = parse_config("default.cfg")
    width = data['data']['WIDTH']
    height = data['data']['HEIGHT']
    entry_point = data['data']['ENTRY']
    exit_point = data['data']['EXIT']

    maze = MazeGrid(width, height)

    maze.create_grid()

    maze.generate(entry_point)

    maze.set_boundaries(entry_point, exit_point)

    maze.save_to_file("maze.txt")

if __name__ == "__main__":
    main()
