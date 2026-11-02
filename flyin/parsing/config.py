from dataclasses import dataclass
from typing import Any, Callable, Optional
from ..models import Hub, Connection
from ..utils import utils
from .config_error import ConfigError, StructError


@dataclass
class Config():
    """Encapsulates parsed configuration state for drones, hubs, and
    connections.
    """

    _zones = ["normal", "restricted", "priority", "blocked"]

    def __init__(self) -> None:
        """Initialize empty configuration state."""
        self._nb_drones: int = 0
        self._hubs: list[Hub] = []
        self._connections: list[Connection] = []
        self._start_hub: Optional[Hub] = None
        self._end_hub: Optional[Hub] = None
        self._current_line: int = 0

    def read_config(self, filename: str) -> list[tuple[int, str, str]]:
        """Read and tokenize a configuration file into
        (line_number, key, value) tuples.

        Args:
            filename (str): Path to configuration file.

        Returns:
            list[tuple[int, str, str]]: Tokenized valid non-comment lines.

        Raises:
            ConfigError: If file cannot be found, read, or decoded.
            StructError: If syntax lacks key-value colon separators.
        """
        cfg: list[tuple[int, str, str]] = []

        try:
            with open(filename, "r") as file:
                for i, raw_line in enumerate(file, start=1):
                    line = raw_line.strip()

                    if not line or line.startswith("#"):
                        continue
                    if ":" not in line:
                        raise StructError(line=i)
                    pairs = line.split(":")
                    if len(pairs) != 2:
                        raise StructError(line=i)
                    if not pairs[0] or not pairs[1]:
                        raise StructError(line=i)
                    cfg.append((i, pairs[0], pairs[1]))

        except FileNotFoundError:
            raise ConfigError(utils.error("File Not Found."))
        except IsADirectoryError:
            raise ConfigError(utils.error("Not a regular file."))
        except PermissionError:
            raise ConfigError(utils.error("Permission denied."))
        except UnicodeDecodeError:
            raise ConfigError(utils.error("Not a readable text file."))

        if len(cfg) < 4:
            raise StructError()
        return cfg

    def to_hub(self, cfg: str) -> Hub:
        """Parse a hub definition string into a Hub object.

        Args:
            cfg (str): The raw string defining the hub and optional metadata.

        Returns:
            Hub: Validated and constructed Hub instance.

        Raises:
            ConfigError: If coordinates or format are invalid.
            StructError: If brackets or criteria are malformed.
        """
        if "[" in cfg:
            if not cfg.endswith("]"):
                raise StructError(utils.error(Hub.EXPECTED_FORMAT),
                                  line=self._current_line)
            mandatory_part, optional_part = cfg[:-1].split("[", 1)
            optional = optional_part.split()
        else:
            mandatory_part = cfg
            optional = []

        mandatory = mandatory_part.split()
        if len(mandatory) != 3:
            raise ConfigError(utils.error(Hub.EXPECTED_FORMAT),
                              line=self._current_line)

        opts = self._hub_optional_criteria(optional)

        return Hub(
            name=self._to_name(mandatory[0]),
            x=self.to_int(mandatory[1], 0, False),
            y=self.to_int(mandatory[2], 0, False),
            zone=opts.get("zone", "normal"),
            color=opts.get("color", "none"),
            max_drones=opts.get("max_drones", 1)
            )

    def to_connection(self, cfg: str, id: int) -> Connection:
        """Parse a connection definition string into a Connection object.

        Args:
            cfg (str): The raw string defining the edge between two hubs.
            id (int): Unique integer index for the connection.

        Returns:
            Connection: Validated and constructed Connection instance.

        Raises:
            ConfigError: If referenced hubs are missing or identical.
            StructError: If brackets or criteria are malformed.
        """
        if "[" in cfg:
            if not cfg.endswith("]"):
                raise StructError(utils.error(Connection.EXPECTED_FORMAT),
                                  line=self._current_line)
            mandatory_part, optional_part = cfg[:-1].split("[", 1)
            optional = optional_part.split()
        else:
            mandatory_part = cfg
            optional = []

        mandatory = mandatory_part.strip().split("-")
        if len(mandatory) != 2:
            raise ConfigError(utils.m_error(Hub.EXPECTED_FORMAT),
                              line=self._current_line)
        elif mandatory[0] == mandatory[1]:
            raise ConfigError(
                utils.m_error("Connections must be between 2 different hubs"),
                line=self._current_line)

        opts = self._con_optional_criteria(optional)

        for c in mandatory:
            if c not in [hub.name for hub in self._hubs]:
                raise ConfigError(
                    utils.m_error(f"'{c}' hub is not defined.") +
                    utils.comment("Defined Hubs:") +
                    utils.comment(
                        f"{', '.join([hub.name for hub in self._hubs])}"),
                    line=self._current_line)

        return Connection(
            id=id,
            hub1=next((h for h in self._hubs if h.name == mandatory[0])),
            hub2=next((h for h in self._hubs if h.name == mandatory[1])),
            max_link_capacity=opts.get("max_link_capacity", 1)
            )

    def _hub_optional_criteria(self, optional: list[str]) -> dict[str, Any]:
        """Parse and validate optional key=value fields for a hub definition.

        Args:
            optional (list[str]): Tokenized optional fields (e.g.
                ['zone=restricted', 'color=blue']).

        Returns:
            dict[str, Any]: Mapping of validated option keys to their values.

        Raises:
            ConfigError: If an unknown, duplicate, or malformed option is
            found.
        """

        CRITERIA: dict[str, Callable[[str], Any]] = {
                "zone": self._to_zone,
                "color": self._to_color,
                "max_drones": lambda val: self.to_int(val, 1, True)
            }

        params = {}
        for item in optional:
            if "=" not in item:
                raise ConfigError(utils.op_error(Hub.EXPECTED_FORMAT),
                                  line=self._current_line)

            key, value = item.split("=", 1)
            if key not in CRITERIA or key in params:
                raise ConfigError(utils.op_error(Hub.EXPECTED_FORMAT),
                                  line=self._current_line)

            params[key] = CRITERIA[key](value)
        return params

    def _con_optional_criteria(self, optional: list[str]) -> dict[str, Any]:
        """Parse and validate optional key=value fields for a connection.

        Args:
            optional (list[str]): Tokenized optional fields (e.g.
                ['max_link_capacity=2']).

        Returns:
            dict[str, Any]: Mapping of validated option keys to their values.

        Raises:
            ConfigError: If an unknown, duplicate, or malformed option is
            found.
        """

        CRITERIA: dict[str, Callable[[str], Any]] = {
                "max_link_capacity": lambda val: self.to_int(val, 1, True)
            }

        params = {}
        for item in optional:
            if "=" not in item:
                raise ConfigError(utils.op_error(Connection.EXPECTED_FORMAT),
                                  line=self._current_line)

            key, value = item.split("=", 1)
            if key not in CRITERIA or key in params:
                raise ConfigError(utils.op_error(Connection.EXPECTED_FORMAT),
                                  line=self._current_line)

            params[key] = CRITERIA[key](value)
        return params

    def to_int(self, info: str, criteria: int, positive: bool) -> int:
        """Parse and validate an integer value with constraints.

        Args:
            info (str): String representation of the number.
            criteria (int): 1 if optional criteria, 0 if mandatory field.
            positive (bool): True if number must be strictly greater than 0.

        Returns:
            int: The parsed integer.

        Raises:
            ConfigError: If input is not a valid integer or violates
            positivity.
        """
        try:
            value = int(info)
            if positive and value <= 0:
                raise ValueError()
            return value

        except ValueError:

            if criteria and positive:
                raise ConfigError(
                    utils.op_error("Value must be a postive integer above zero"
                                   f'''\nInput: "{info}"'''),
                    line=self._current_line)
            elif criteria and not positive:
                raise ConfigError(
                    utils.op_error("Value must be an integer."
                                   f'''\nInput: "{info}"'''),
                    line=self._current_line)

            elif not criteria and positive:
                raise ConfigError(
                    utils.m_error("Value must be a postive integer above zero."
                                  f'''\nInput: "{info}"'''),
                    line=self._current_line)
            else:
                raise ConfigError(
                    utils.m_error("Value must be an integer."
                                  f'''\nInput: "{info}"'''),
                    line=self._current_line)

    def _to_name(self, info: str) -> str:
        """Validate and return a hub name, rejecting spaces and dashes.

        Args:
            info (str): Raw name string to validate.

        Returns:
            str: The validated name.

        Raises:
            ConfigError: If the name contains a space or dash.
        """

        if " " in info or "-" in info:

            raise ConfigError(
                utils.m_error("Hub names can use any valid characters except:"
                              f'''\n  • {utils.bold("dashes('-')")};'''
                              f'''\n  • {utils.bold("spaces(' ')")}.'''
                              f"\nInput: '{info}'"),
                line=self._current_line)

        return info

    def _to_zone(self, info: str) -> str:
        """Validate and return a zone type string.

        Args:
            info (str): Raw zone string to validate.

        Returns:
            str: The validated zone type.

        Raises:
            ConfigError: If the zone type is not one of the supported values.
        """

        if info not in self._zones:

            raise ConfigError(
                utils.op_error('''String must be a zone type.'''
                               f'''\nInput: "{info}"\n''') +
                utils.comment(f'''Zone types available: '''
                              f'''\n{", ".join(self._zones)}.'''),
                line=self._current_line)

        return info

    def _to_color(self, info: str) -> str:
        """Validate and return a color string.

        Args:
            info (str): Raw color string to validate.

        Returns:
            str: The validated color string.

        Raises:
            ConfigError: If the color contains spaces or dashes.
        """

        if " " in info or "-" in info:
            raise ConfigError(
                utils.op_error("Color must be a single-word string without "
                               "spaces or dashes."
                               f'\nInput: "{info}"'),
                line=self._current_line
            )
        return info

    @property
    def nb_drones(self) -> int:
        """Return the number of drones for the simulation."""
        return self._nb_drones

    @property
    def hubs(self) -> list[Hub]:
        """Return the list of all parsed hubs."""
        return self._hubs

    @property
    def connections(self) -> list[Connection]:
        """Return the list of all parsed connections."""
        return self._connections

    @property
    def current_line(self) -> int:
        """Return the current line number being parsed."""
        return self._current_line

    @property
    def start_hub(self) -> Optional[Hub]:
        """Return the designated start hub, or None if not yet set."""
        return self._start_hub

    @property
    def end_hub(self) -> Optional[Hub]:
        """Return the designated end hub, or None if not yet set."""
        return self._end_hub
