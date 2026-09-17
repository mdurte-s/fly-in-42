class ConfigError(Exception):
    pass


class Config():
    nb_drones: int = 0
    hubs: list[dict[str, tuple[int, int, str, str, int]]] = []
    connections: list[tuple[str, str]] = []

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
            "lime"
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
                    raise ConfigError(f"expected BLA BLA BLA, got {line}")
                pairs = line.split(":")
                if len(pairs) != 2:
                    raise ConfigError(f"expected BLA BLA BLA, got {line}")
                if not pairs[0] or not pairs[1]:
                    raise ConfigError(f"expected BLA BLA BLA, got {line}")
                config.append((pairs[0], pairs[1]))

    except FileNotFoundError:
        raise ConfigError("File Not Found")
    except IsADirectoryError:
        raise ConfigError("Not a regular file")
    except PermissionError:
        raise ConfigError("Permission denied")
    except UnicodeDecodeError:
        raise ConfigError("Not a readable text file")

    return config
