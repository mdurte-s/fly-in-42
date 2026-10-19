from ..models import Hub, Connection
from ..utils import utils
from .config import Config
from .config_error import ConfigError, StructError


class MapParser():
    """Parser responsible for reading, validating, and converting map files
    into Config.
    """

    def __init__(self, filepath: str) -> None:
        """Initialize the map parser with a target file path.

        Args:
            filepath (str): Path to the map configuration file.
        """
        self._filepath: str = filepath
        self._cfg: Config = self._parser()

    def _parser(self) -> Config:
        """Parse configuration tokens into validated hubs, connections, and
        drones.

        Returns:
            Config: Fully validated Config instance.

        Raises:
            ConfigError: If duplicate hubs, coordinates, or connections are
            found.
            StructError: If syntax or structure requirements are violated.
        """
        cfg = Config()
        config: list[tuple[int, str, str]] = cfg.read_config(self._filepath)
        conn_count: int = 0
        connections_started: bool = False

        for line, key, val in config:
            cfg._current_line = line

            if not cfg.nb_drones:
                if key == "nb_drones":
                    cfg._nb_drones = cfg.to_int(val.strip(), 0, True)
                    continue
                else:
                    raise StructError(line=line)

            if key in ("start_hub", "end_hub", "hub"):
                if connections_started:
                    raise StructError(line=line)

                if key == "start_hub" and cfg.start_hub is not None:
                    raise ConfigError(
                        utils.error("Multiple start hubs defined."),
                        line=line
                    )
                elif key == "end_hub" and cfg.end_hub is not None:
                    raise ConfigError(
                        utils.error("Multiple end hubs defined."),
                        line=line
                    )

                new_hub: Hub = cfg.to_hub(val.strip())

                if new_hub.name in [hub.name for hub in cfg.hubs]:
                    raise ConfigError(
                        utils.error(f"Hub named '{new_hub.name}'"
                                    "already exists."),
                        line=line
                    )

                if new_hub.coordinates in [h.coordinates for h in cfg.hubs]:
                    raise ConfigError(
                        utils.error(f"Hub at {new_hub.coordinates}"
                                    "already exists."),
                        line=line
                    )

                cfg.hubs.append(new_hub)
                if key == "start_hub":
                    cfg._start_hub = new_hub
                elif key == "end_hub":
                    cfg._end_hub = new_hub

            elif key == "connection":
                if cfg.start_hub is None:
                    raise StructError(message="Missing start_hub!", line=line)
                if cfg.end_hub is None:
                    raise StructError(message="Missing end_hub!", line=line)

                connections_started = True
                new_connection: Connection = cfg.to_connection(
                    val.strip(), conn_count
                )
                n = {new_connection.hub1.name, new_connection.hub2.name}

                if n in [{c.hub1.name, c.hub2.name} for c in cfg.connections]:
                    raise ConfigError(
                        utils.m_error(
                            f"Connection '{new_connection.hub1.name}"
                            f"-{new_connection.hub2.name}' already exists."
                        ),
                        line=line
                    )

                cfg.connections.append(new_connection)
                conn_count += 1

            else:
                raise StructError(line=line)

        if cfg.start_hub is None:
            raise StructError(message="Missing start_hub!")
        if cfg.end_hub is None:
            raise StructError(message="Missing end_hub!")
        if conn_count == 0:
            raise StructError(message="Missing connections!")

        return cfg

    @property
    def cfg(self) -> Config:
        """Return the parsed Config instance."""
        return self._cfg
