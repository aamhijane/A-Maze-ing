from parse_config import config_parsing


def main() -> None:

    data = config_parsing("config.txt")

    print(data)


if __name__ == "__main__":
    main()
