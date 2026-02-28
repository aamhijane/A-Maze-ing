

class InvalidConfigError(Exception):
    """Base config exception."""
    pass


class InvalidEntryError(InvalidConfigError):
    pass


class InvalidFileError(InvalidConfigError):
    pass


class InvalidArgumentError(InvalidConfigError):
    pass
