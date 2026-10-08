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
        hub_started: bool = False
        hub_ended: bool = False

        for line, key, val in config:
            cfg._current_line = line
            if key == "nb_drones" and not hub_started:
                cfg._nb_drones = cfg.to_int(val.strip(), 0, True)

            elif (key == "start_hub" and cfg._nb_drones >= 0 and
                    not hub_started and not hub_ended):
                new_hub: Hub = cfg.to_hub(val.strip())
                cfg._hubs.append(new_hub)
                hub_started = True

            elif ((key == "hub" or key == "end_hub")
                    and hub_started and not hub_ended):
                new_hub: Hub = cfg.to_hub(val.strip())
                if new_hub.name in [hub.name for hub in cfg._hubs]:
                    raise ConfigError(
                        utils.error(f"Hub named '{new_hub.name}' "
                                    "already exists."),
                        line=line)
                if (new_hub.coordinates in [hub.coordinates
                                            for hub in cfg._hubs]):
                    raise ConfigError(
                        utils.error(f"Hub at {new_hub.coordinates} "
                                    "already exists."),
                        line=line)
                cfg._hubs.append(new_hub)
                hub_ended = (True if key == "end_hub" else False)

            elif key == "connection" and hub_ended:
                new_connection: Connection = cfg.to_connection(val.strip())
                new = {new_connection.hub1.name, new_connection.hub2.name}
                if new in [{c.hub1.name, c.hub2.name}
                           for c in cfg._connections]:
                    raise ConfigError(
                        utils.m_error(
                            f"Connection '{new_connection.hub1.name}"
                            f"-{new_connection.hub2.name}' "
                            "already exists."),
                        line=line)
                cfg._connections.append(new_connection)

            else:
                raise StructError(line=line)

        return (cfg)

    @property
    def cfg(self) -> Config:
        return self._cfg
