from dataclasses import dataclass, field
from .hubs import Hub
from .utils import comment, error

usage = comment("Usage: ./main.py <path/config-file.txt>")
struct = (f"{comment('Configuration file expected structure:')}\n"
          "\nnb_drones: NB_DRONES"
          "\nstart_hub: NAME X Y [OPTIONAL_CRITERIA]"
          "\nhub: NAME X Y [OPTIONAL_CRITERIA]"
          "\n[...]"
          "\nend_hub: NAME X Y [OPTIONAL_CRITERIA]"
          "\nconnection: NAME-NAME [OPTIONAL_CRITERIA]"
          "\n[...]\n"
          f"{comment('\nHub OPTIONAL_CRITERIA: ')}"
          f"{comment('\n[zone=ZONE color=COLOR max_drones=MAX_DRONES]')}"
          f"{comment('\nConnection OPTIONAL_CRITERIA: ')}"
          f"{comment('\n[max_link_capacity=MAX_LINK_CAPACITY]')}")

hub = "Expected: 'hub: NAME X Y [OPTIONAL_CRITERIA]'"
connection = "Expected: 'connection: NAME-NAME [OPTIONAL_CRITERIA]'"


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

    def __init__(self, message: str = struct) -> None:
        """Initialize the exception with a message."""
        super().__init__(message)


@dataclass
class Config():
    nb_drones: int = -1
    hubs: list[Hub] | None = None
    hub_names: list[str] = []
    connections: list[tuple[str, str, int]] = None

    colors = [
            "blue",
            "red",
            "green",
            "purple",
            "yellow",
            "orange",
            "cyan",
            "magenta",
            "gold",
            "brown",
            "lime",
            "pink"
            ]

    zones = ["restricted", "priority"]


def read_config(filename: str) -> list[tuple[str, str]]:
    config: list[tuple[str, str]] = []

    try:
        with open(filename, "r") as file:
            for raw_line in file:
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue
                if ":" not in line:
                    raise StructError()
                pairs = line.split(":")
                if len(pairs) != 2:
                    raise StructError()
                if not pairs[0] or not pairs[1]:
                    raise StructError()
                config.append((pairs[0], pairs[1]))

    except FileNotFoundError:
        raise ConfigError(error("File Not Found."))
    except IsADirectoryError:
        raise ConfigError(error("Not a regular file."))
    except PermissionError:
        raise ConfigError(error("Permission denied."))
    except UnicodeDecodeError:
        raise ConfigError(error("Not a readable text file."))

    return config
