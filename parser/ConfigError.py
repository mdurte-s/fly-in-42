from . import utils

usage = utils.comment("Usage: ./main.py <path/config-file.txt>")
struct = (f"{utils.comment('Configuration file expected structure:')}\n"
          "\nnb_drones: NB_DRONES"
          "\nstart_hub: NAME X Y [OPTIONAL_CRITERIA]"
          "\nhub: NAME X Y [OPTIONAL_CRITERIA]"
          "\n[...]"
          "\nend_hub: NAME X Y [OPTIONAL_CRITERIA]"
          "\nconnection: NAME-NAME [OPTIONAL_CRITERIA]"
          "\n[...]\n"
          f"{utils.comment('Hub OPTIONAL_CRITERIA: ')}"
          f"{utils.comment('[zone=ZONE color=COLOR max_drones=MAX_DRONES]')}"
          f"{utils.comment('Connection OPTIONAL_CRITERIA: ')}"
          f"{utils.comment('[max_link_capacity=MAX_LINK_CAPACITY]')}")


class ConfigError(Exception):
    """Raised when the configuration file is invalid."""

    def __init__(self, message: str = "[Configuration Error]") -> None:
        """Initialize the exception with a message."""
        super().__init__(message)


class StructError(ConfigError):
    """Raised when the STRUCTURE of the configuration file is invalid."""

    def __init__(self, message: str = usage) -> None:
        """Initialize the exception with a message."""
        super().__init__(message)


class UsageError(ConfigError):
    """Raised when the USAGE is invalid."""

    def __init__(self, message: str = usage) -> None:
        """Initialize the exception with a message."""
        super().__init__(message)
