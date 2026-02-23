from config_parser import parse_config

def main() -> None:
    data = parse_config("default.cfg")
    print(data)


if __name__ == "__main__":
    main()
