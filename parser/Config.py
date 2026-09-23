from dataclasses import dataclass
from .ConfigError import ConfigError, StructError
from .Hub import Hub
from .Connection import Connection
from . import utils


@dataclass
class Config():

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

    def __init__(self,
                 nb_drones: int = -1,
                 hubs: list[Hub] = [],
                 hub_names: list[str] = [],
                 connections: list[Connection] = []) -> None:

        self._nb_drones: int = nb_drones
        self._hubs: list[Hub] = hubs
        self._hub_names: list[str] = hub_names
        self._connections: list[Connection] = connections

    def read_config(self, filename: str) -> list[tuple[str, str]]:
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
            raise ConfigError(utils.error("File Not Found."))
        except IsADirectoryError:
            raise ConfigError(utils.error("Not a regular file."))
        except PermissionError:
            raise ConfigError(utils.error("Permission denied."))
        except UnicodeDecodeError:
            raise ConfigError(utils.error("Not a readable text file."))

        return config

    def to_hub(self, config: str) -> Hub:

        if "[" in config:
            if not config.endswith("]"):
                raise StructError(utils.error(Hub.hub))
            mandatory_part, optional_part = config[:-1].split("[", 1)
            optional = optional_part.split()
        else:
            mandatory_part = config
            optional = []

        mandatory = mandatory_part.split()
        if len(mandatory) != 3:
            raise ConfigError(utils.m_error(Hub.hub))

        opts = self.parse_optional_params(optional)

        return Hub(
            name=self.to_name(mandatory[0]),
            x=self.to_int(mandatory[1], 0, False),
            y=self.to_int(mandatory[2], 0, False),
            zone=opts.get("zone", ""),
            color=opts.get("color", ""),
            max_drones=opts.get("max_drones", "")
            )

    def to_connection(self, config: str) -> Connection:

        info = config.split()
        if not info or len(info) > 2:
            raise StructError(utils.error(Connection.connection))

        max_link = (self.to_int(info[1], 1, True) if len(info) == 2 else -1)

        con = info[0].split("-")
        if len(con) != 2:
            raise StructError(utils.error(Connection.connection))

        for c in con:
            if c not in self._hub_names:
                raise ConfigError(
                    utils.m_error(f"'{c}' hub is not defined.") +
                    utils.comment("Defined Hubs:") +
                    utils.comment(f"{', '.join(self._hub_names)}"))

        return Connection(
            hub1=con[0],
            hub2=con[1],
            max_link_capacity=max_link
            )

    def parse_optional_params(self, optional: list[str]) -> dict:

        OPTIONAL_PARSERS = {
                "zone": self.to_zone,
                "color": self.to_color,
                "max_drones": lambda val: self.to_int(val, 1, True)
            }

        params = {}
        for item in optional:
            if "=" not in item:
                raise ConfigError(utils.op_error(Hub.hub))

            key, value = item.split("=", 1)
            if key not in OPTIONAL_PARSERS or key in params:
                raise ConfigError(utils.op_error(Hub.hub))

            params[key] = OPTIONAL_PARSERS[key](value)
        return params

    def to_int(self, info: str, criteria: int, positive: bool) -> int:

        try:
            value = int(info)
            if positive and value <= 0:
                raise ValueError()
            return value

        except ValueError:

            if criteria and positive:
                raise ConfigError(
                    utils.op_error("Value must be a postive integer above zero"
                                   f'''\nInput: "{info}"'''))
            elif criteria and not positive:
                raise ConfigError(
                    utils.op_error("Value must be an integer."
                                   f'''\nInput: "{info}"'''))

            elif not criteria and positive:
                raise ConfigError(
                    utils.m_error("Value must be a postive integer above zero."
                                  f'''\nInput: "{info}"'''))
            else:
                raise ConfigError(
                    utils.m_error("Value must be an integer."
                                  f'''\nInput: "{info}"'''))

    def to_name(self, info: str) -> str:

        if " " in info or "-" in info:

            raise ConfigError(
                utils.m_error("Hub names can use any valid characters except:"
                              f'''\n  • {utils.bold("dashes('-')")};'''
                              f'''\n  • {utils.bold("spaces(' ')")}.'''
                              f"\nInput: '{info}'"))

        return info

    def to_zone(self, info: str) -> str:

        if info not in Config.zones:

            raise ConfigError(
                utils.op_error('''String must be a zone type.'''
                               f'''\nInput: "{info}"\n''') +
                utils.comment(f'''Zone types available: '''
                              f'''\n{", ".join(self.zones)}.'''))

        return info

    def to_color(self, info: str) -> str:

        if info not in self.colors:
            raise ConfigError(
                utils.op_error('''String must be a color.'''
                               f'''\nInput: "{info}"\n''') +
                utils.comment('''Colors available: ''') +
                utils.comment(f'''\n{", ".join(self.colors)}.'''))

        return info
