from dataclasses import dataclass
from ..models import Hub, Connection
from ..utils import utils
from .config_error import ConfigError, StructError


@dataclass
class Config():

    _colors = [
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

    _zones = ["normal", "restricted", "priority", "blocked"]

    def __init__(self) -> None:
        self._nb_drones: int = -1
        self._hubs: list[Hub] = []
        self._connections: list[Connection] = []

    def read_config(self, filename: str) -> list[tuple[str, str]]:
        cfg: list[tuple[str, str]] = []

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
                    cfg.append((pairs[0], pairs[1]))

        except FileNotFoundError:
            raise ConfigError(utils.error("File Not Found."))
        except IsADirectoryError:
            raise ConfigError(utils.error("Not a regular file."))
        except PermissionError:
            raise ConfigError(utils.error("Permission denied."))
        except UnicodeDecodeError:
            raise ConfigError(utils.error("Not a readable text file."))

        return cfg

    def to_hub(self, cfg: str) -> Hub:

        if "[" in cfg:
            if not cfg.endswith("]"):
                raise StructError(utils.error(Hub.EXPECTED_FORMAT))
            mandatory_part, optional_part = cfg[:-1].split("[", 1)
            optional = optional_part.split()
        else:
            mandatory_part = cfg
            optional = []

        mandatory = mandatory_part.split()
        if len(mandatory) != 3:
            raise ConfigError(utils.m_error(Hub.EXPECTED_FORMAT))

        opts = self.hub_optional_criteria(optional)

        return Hub(
            name=self.to_name(mandatory[0]),
            x=self.to_int(mandatory[1], 0, False),
            y=self.to_int(mandatory[2], 0, False),
            zone=opts.get("zone", ""),
            color=opts.get("color", ""),
            max_drones=opts.get("max_drones", "")
            )

    def to_connection(self, cfg: str) -> Connection:

        if "[" in cfg:
            if not cfg.endswith("]"):
                raise StructError(utils.error(Connection.EXPECTED_FORMAT))
            mandatory_part, optional_part = cfg[:-1].split("[", 1)
            optional = optional_part.split()
        else:
            mandatory_part = cfg
            optional = []

        mandatory = mandatory_part.strip().split("-")
        if len(mandatory) != 2:
            raise ConfigError(utils.m_error(Hub.hub))
        elif mandatory[0] == mandatory[1]:
            raise ConfigError(
                utils.m_error("Connections must be between 2 different hubs"))

        opts = self.con_optional_criteria(optional)

        for c in mandatory:
            if c not in [hub._name for hub in self._hubs]:
                raise ConfigError(
                    utils.m_error(f"'{c}' hub is not defined.") +
                    utils.comment("Defined Hubs:") +
                    utils.comment(
                        f"{', '.join([hub._name for hub in self._hubs])}"))

        return Connection(
            hub1=next((h for h in self._hubs if h._name == mandatory[0])),
            hub2=next((h for h in self._hubs if h._name == mandatory[1])),
            max_link_capacity=opts.get("max_link_capacity", "")
            )

    def _hub_optional_criteria(self, optional: list[str]) -> dict:

        CRITERIA = {
                "zone": self.to_zone,
                "color": self.to_color,
                "max_drones": lambda val: self.to_int(val, 1, True)
            }

        params = {}
        for item in optional:
            if "=" not in item:
                raise ConfigError(utils.op_error(Hub.EXPECTED_FORMAT))

            key, value = item.split("=", 1)
            if key not in CRITERIA or key in params:
                raise ConfigError(utils.op_error(Hub.EXPECTED_FORMAT))

            params[key] = CRITERIA[key](value)
        return params

    def _con_optional_criteria(self, optional: list[str]) -> dict:

        CRITERIA = {
                "max_link_capacity": lambda val: self.to_int(val, 1, True)
            }

        params = {}
        for item in optional:
            if "=" not in item:
                raise ConfigError(utils.op_error(Connection.EXPECTED_FORMAT))

            key, value = item.split("=", 1)
            if key not in CRITERIA or key in params:
                raise ConfigError(utils.op_error(Connection.EXPECTED_FORMAT))

            params[key] = CRITERIA[key](value)
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

    def _to_name(self, info: str) -> str:

        if " " in info or "-" in info:

            raise ConfigError(
                utils.m_error("Hub names can use any valid characters except:"
                              f'''\n  • {utils.bold("dashes('-')")};'''
                              f'''\n  • {utils.bold("spaces(' ')")}.'''
                              f"\nInput: '{info}'"))

        return info

    def _to_zone(self, info: str) -> str:

        if info not in self._zones:

            raise ConfigError(
                utils.op_error('''String must be a zone type.'''
                               f'''\nInput: "{info}"\n''') +
                utils.comment(f'''Zone types available: '''
                              f'''\n{", ".join(self._zones)}.'''))

        return info

    def _to_color(self, info: str) -> str:

        if info not in self._colors:
            raise ConfigError(
                utils.op_error('''String must be a color.'''
                               f'''\nInput: "{info}"\n''') +
                utils.comment('''Colors available: ''') +
                utils.comment(f'''\n{", ".join(self._colors)}.'''))

        return info
