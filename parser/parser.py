from .config import Config, ConfigError, StructError, read_config
from .hubs import to_hub
from .connections import to_connection
from .utils import to_int, error, m_error


def parser(filename: str) -> Config:

    config = read_config(filename)
    cfg = Config()
    hub_started: bool = False
    hub_ended: bool = False 
    connects: list[tuple(str, str)] = []

    for item in config:
        if item[0] == "nb_drones" and not hub_started and not hub_ended:
            cfg.nb_drones = to_int(item[1].strip(), 0, True)

        elif (item[0] == "start_hub" and cfg.nb_drones >= 0 and
              not hub_started and not hub_ended):
            new_hub = to_hub(item[1].strip())
            cfg.hub_names.append(list(new_hub.keys())[0])
            cfg.hubs.append(new_hub)
            hub_started = True

        elif ((item[0] == "hub" or item[0] == "end_hub")
              and hub_started and not hub_ended):
            new_hub = to_hub(item[1].strip())
            new_hub_name = list(new_hub.keys())[0]
            if new_hub_name in cfg.hub_names:
                raise ConfigError(
                    error(f'''Hub named "{new_hub_name}" already exists.''')
                )
            cfg.hub_names.append(new_hub_name)
            cfg.hubs.append(new_hub)
            hub_ended = (True if item[0] == "end_hub" else False)

        elif item[0] == "connection" and hub_started and hub_ended:
            new_connection = to_connection(item[1].strip(), cfg.hub_names)
            new = {new_connection[0], new_connection[1]}
            existing_cons = [{c[0], c[1]} for c in cfg.connections]
            if new in existing_cons:
                raise ConfigError(
                    m_error(f"Connection '{new_connection[0]}"
                            f"-{new_connection[1]}' already exists."))
            cfg.connections.append(new_connection)

        else:
            raise StructError()

    return (cfg)
