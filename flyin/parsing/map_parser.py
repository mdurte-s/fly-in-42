from ..models import Hub, Connection
from ..utils import utils
from .config import Config
from .config_error import ConfigError, StructError


class MapParser():

    def __init__(self, filepath: str) -> None:
        self._filepath: str = filepath
        self._cfg: Config = self._parser()

    def _parser(self) -> Config:

        cfg = Config()
        config: list[tuple[int, str, str]] = cfg.read_config(self._filepath)
        hub_init: bool = False
        hub_end: bool = False

        for line, key, val in config:
            cfg._current_line = line

            if key == "nb_drones" and not cfg.nb_drones and not hub_init:
                cfg._nb_drones = cfg.to_int(val.strip(), 0, True)

            elif (cfg.nb_drones and key == "start_hub" and not hub_init):
                new_start_hub: Hub = cfg.to_hub(val.strip())
                cfg.hubs.append(new_start_hub)
                hub_init = True

            elif ((key == "hub" or key == "end_hub") and hub_init and
                  not hub_end):
                new_hub: Hub = cfg.to_hub(val.strip())

                if new_hub.name in [hub.name for hub in cfg.hubs]:
                    raise ConfigError(utils.error(
                        f"Hub named '{new_hub.name}' already exists."),
                        line=line
                        )

                if (new_hub.coordinates in [h.coordinates for h in cfg.hubs]):
                    raise ConfigError(utils.error(
                        f"Hub at {new_hub.coordinates} already exists."),
                        line=line
                        )

                cfg.hubs.append(new_hub)
                hub_end = (True if key == "end_hub" else False)

            elif key == "connection" and hub_end:
                new_connection: Connection = cfg.to_connection(val.strip())
                n = {new_connection.hub1.name, new_connection.hub2.name}

                if n in [{c.hub1.name, c.hub2.name} for c in cfg.connections]:
                    raise ConfigError(utils.m_error(
                        f"Connection '{new_connection.hub1.name}"
                        f"-{new_connection.hub2.name}' already exists."),
                        line=line
                        )

                cfg.connections.append(new_connection)

            else:
                raise StructError(line=line)

        if not cfg.nb_drones:
            raise StructError(message="Missing parameter nb_drones.")
        if not cfg.hubs:
            raise StructError(message="Missing parameters hubs.")
        if not cfg.connections:
            raise StructError(message="Missing parameters connections.")
        return (cfg)

    @property
    def cfg(self) -> Config:
        return self._cfg
