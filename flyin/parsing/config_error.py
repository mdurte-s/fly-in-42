from typing import Optional
from ..utils import comment, bold


class ConfigError(Exception):
    """ Raised when the configuration file is invalid. """

    def __init__(
            self, message: str = "Configuration Error",
            line: Optional[int] = None
            ) -> None:
        """ Initialize the exception with a message. """

        if line:
            full_message = f"{bold(f'[Line {line}]')} {message}"
        else:
            full_message = message
        super().__init__(full_message)


class StructError(ConfigError):
    """ Raised when the STRUCTURE of the configuration file is invalid. """

    EXPECTED_FORMAT = (
        f"{comment('Configuration file expected structure:')}\n"
        "\nnb_drones: NB_DRONES"
        "\nstart_hub: NAME X Y [OPTIONAL_CRITERIA]"
        "\nhub: NAME X Y [OPTIONAL_CRITERIA]"
        "\n[...]"
        "\nend_hub: NAME X Y [OPTIONAL_CRITERIA]"
        "\nconnection: NAME-NAME [OPTIONAL_CRITERIA]"
        "\n[...]\n"
        f"{comment('Hub OPTIONAL_CRITERIA: ')}"
        f"{comment('[zone=ZONE color=COLOR max_drones=MAX_DRONES]')}"
        f"{comment('Connection OPTIONAL_CRITERIA: ')}"
        f"{comment('[max_link_capacity=MAX_LINK_CAPACITY]')}"
        )

    def __init__(
            self, message: str = EXPECTED_FORMAT, line: Optional[int] = None
            ) -> None:
        """ Initialize the exception with a message. """

        if line:
            full_message = f"{bold(f'[Line {line}]')} {message}"
        else:
            full_message = message
        super().__init__(full_message)


class UsageError(ConfigError):
    """ Raised when the USAGE is invalid. """

    EXPECTED_FORMAT = comment("Usage: ./main.py <path/config-file.txt>")

    def __init__(self,
                 message: str = EXPECTED_FORMAT,
                 ) -> None:
        """ Initialize the exception with a message. """

        super().__init__(message)
