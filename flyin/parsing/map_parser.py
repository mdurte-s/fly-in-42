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
        config: list[tuple[str, str]] = cfg.read_config(self._filepath)
        hub_started: bool = False
        hub_ended: bool = False

        for item in config:
            if item[0] == "nb_drones" and not hub_started:
                cfg._nb_drones = cfg.to_int(item[1].strip(), 0, True)

            elif (item[0] == "start_hub" and cfg._nb_drones >= 0 and
                  not hub_started and not hub_ended):
                new_hub: Hub = cfg.to_hub(item[1].strip())
                cfg._hubs.append(new_hub)
                hub_started = True

            elif ((item[0] == "hub" or item[0] == "end_hub")
                  and hub_started and not hub_ended):
                new_hub: Hub = cfg.to_hub(item[1].strip())
                if new_hub._name in [hub._name for hub in cfg._hubs]:
                    raise ConfigError(
                        utils.error(f"Hub named '{new_hub._name}' "
                                    "already exists."))
                if ((new_hub._x, new_hub._y) in
                   [(hub._x, hub._y) for hub in cfg._hubs]):
                    raise ConfigError(
                        utils.error(f"Hub at ({new_hub._x}, {new_hub._y}) "
                                    "already exists."))
                cfg._hubs.append(new_hub)
                hub_ended = (True if item[0] == "end_hub" else False)

            elif item[0] == "connection" and hub_ended:
                new_connection: Connection = cfg.to_connection(item[1].strip())
                new = {new_connection._hub1._name, new_connection._hub2._name}
                if new in [{c._hub1._name, c._hub2._name}
                           for c in cfg._connections]:
                    raise ConfigError(
                        utils.m_error(
                            f"Connection '{new_connection._hub1._name}"
                            f"-{new_connection._hub2._name}' already exists."))
                cfg._connections.append(new_connection)

            else:
                raise StructError()

        return (cfg)
