from ..models import Hub, Connection
from ..utils import utils
from .config import Config
from .config_error import ConfigError, StructError


class MapParser():

    def __init__(self,
                 filepath: str
                 ) -> None:
        self._filepath: str = filepath

    def parser(self) -> Config:

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
                if new_hub._name in [hub._name for hub in cfg._hubs]:
                    raise ConfigError(
                        utils.error(f"Hub named '{new_hub._name}' "
                                    "already exists."),
                        line=line)
                if ((new_hub._x, new_hub._y) in [(hub._x, hub._y)
                                                 for hub in cfg._hubs]):
                    raise ConfigError(
                        utils.error(f"Hub at ({new_hub._x}, {new_hub._y}) "
                                    "already exists."),
                        line=line)
                cfg._hubs.append(new_hub)
                hub_ended = (True if key == "end_hub" else False)

            elif key == "connection" and hub_ended:
                new_connection: Connection = cfg.to_connection(val.strip())
                new = {new_connection._hub1._name, new_connection._hub2._name}
                if new in [{c._hub1._name, c._hub2._name}
                           for c in cfg._connections]:
                    raise ConfigError(
                        utils.m_error(
                            f"Connection '{new_connection._hub1._name}"
                            f"-{new_connection._hub2._name}' "
                            "already exists."),
                        line=line)
                cfg._connections.append(new_connection)

            else:
                raise StructError(line=line)

        return (cfg)
