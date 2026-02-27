from validate_config import validate

def main() -> None:

    path = "config.txt"
    status = validate(path)['status']

    if status == "success":
        data = validate(path)['data']

        print(data)
    else:
        print(validate(path)['error'])

if __name__ == "__main__":
    main()
