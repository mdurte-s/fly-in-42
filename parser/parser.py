from .Config import Config
from .ConfigError import ConfigError, StructError
from . import utils


def parser(filename: str) -> Config:

    cfg = Config()
    config: list[tuple[str, str]] = cfg.read_config(filename)
    hub_started: bool = False
    hub_ended: bool = False

    for item in config:
        if item[0] == "nb_drones" and not hub_started:
            cfg._nb_drones = cfg.to_int(item[1].strip(), 0, True)

        elif (item[0] == "start_hub" and cfg._nb_drones >= 0 and
              not hub_started and not hub_ended):
            new_hub = cfg.to_hub(item[1].strip())
            cfg._hub_coords.append((new_hub._x, new_hub._y))
            cfg._hub_names.append(new_hub._name)
            cfg._hubs.append(new_hub)
            hub_started = True

        elif ((item[0] == "hub" or item[0] == "end_hub")
              and hub_started and not hub_ended):
            new_hub = cfg.to_hub(item[1].strip())
            if new_hub._name in cfg._hub_names:
                raise ConfigError(
                    utils.error(f"Hub named '{new_hub._name}' "
                                "already exists."))
            if (new_hub._x, new_hub._y) in cfg._hub_coords:
                raise ConfigError(
                    utils.error(f"Hub at ({new_hub._x}, {new_hub._y}) "
                                "already exists."))
            cfg._hub_coords.append((new_hub._x, new_hub._y))
            cfg._hub_names.append(new_hub._name)
            cfg._hubs.append(new_hub)
            hub_ended = (True if item[0] == "end_hub" else False)

        elif item[0] == "connection" and hub_ended:
            new_connection = cfg.to_connection(item[1].strip())
            new = {new_connection._hub1, new_connection._hub2}
            existing_cons = [{c._hub1, c._hub2} for c in cfg._connections]
            if new in existing_cons:
                raise ConfigError(
                    utils.m_error(f"Connection '{new_connection[0]}"
                                  f"-{new_connection[1]}' already exists."))
            cfg._connections.append(new_connection)

        else:
            raise StructError()

    return (cfg)
