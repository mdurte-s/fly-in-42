# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   main.py                                             :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: mdurte-s <mdurte-s@student.42porto.com>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/09/11 10:38:28 by mdurte-s           #+#    #+#             #
#   Updated: 2026/09/11 13:16:55 by mdurte-s          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from sys import argv
from dataclasses import dataclass, field


class ConfigError(Exception):
    pass


@dataclass
class Config():
    nb_drones: int = 0
    hubs: list[dict[str, tuple[int, int, str]]] = field(default_factory=list)
    connections: list[dict[str, str]] = field(default_factory=list)


def read_config(filename: str) -> dict[str, str]:
    config: dict[str, str] = {}

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
                config[pairs[0]] = pairs[1]

    except FileNotFoundError:
        raise ConfigError("File Not Found")
    except IsADirectoryError:
        raise ConfigError("Not a regular file")
    except PermissionError:
        raise ConfigError("Permission denied")
    except UnicodeDecodeError:
        raise ConfigError("Not a readable text file")
    return config


def to_int(nb: str) -> int:
    try:
        return int(nb)
    except ValueError:
        raise ConfigError("must be an int")


def to_hub(config: str) -> dict[str, tuple[int, int, str]]:

    new_hub: dict[str, tuple[int, int, str]] = {}
    info = config.split()
    if len(info) != 4:
        raise ConfigError("expected BLA BLA BLA, got not BLA BLA BLA")
    new_hub[info[0]] = (to_int(info[1]), to_int(info[2]), info[3])
    return new_hub


def to_connection(config: str) -> dict[str, str]:

    new_connection: dict[str, str] = {}
    info = config.split("-")
    if len(info) != 2:
        raise ConfigError("expected BLA BLA BLA, got not BLA BLA BLA")
    new_connection[info[0]] = info[1]

def parser(filename: str) -> Config:

    config = read_config(filename)
    cfg = Config()
    hub_started: bool = False
    hub_ended: bool = False
    connection_count: int = 0

    for key in config:
        if key == "nb_drones":
            cfg.nb_drones = to_int(config[key].strip())

        elif key == "start_hub":
            cfg.hubs.append(to_hub(config[key].strip()))
            hub_started = True

        elif key == "hub" and hub_started and not hub_ended:
            cfg.hubs.append(to_hub(config[key].strip()))

        elif key == "end_hub":
            cfg.hubs.append(to_hub(config[key].strip()))
            hub_ended = True

        elif key == "connection":
            connection_count += 1

        else:
            raise ConfigError("expected BLA BLA BLA, got not BLA BLA BLA")
    return (cfg)


def main(args: list[str]) -> int:

    if len(args) != 2:
        return (0)
    cfg = parser(args[1])
    print(cfg.nb_drones)
    print(cfg.hubs)
    return (0)


if __name__ == "__main__":
    main(argv)
