from .config import Config, ConfigError, read_config
from .hubs import to_hub, to_int
from .connections import to_connection
from .utils import comment, error


def parser(filename: str) -> Config:

    config = read_config(filename)
    cfg = Config()
    hub_started: bool = False
    hub_ended: bool = False

    for item in config:
        if item[0] == "nb_drones" and not hub_started and not hub_ended:
            cfg.nb_drones = to_int(item[1].strip())

        elif item[0] == "start_hub" and not hub_started and not hub_ended:
            cfg.hubs.append(to_hub(item[1].strip()))
            hub_started = True

        elif ((item[0] == "hub" or item[0] == "end_hub")
              and hub_started and not hub_ended):
            new_hub = to_hub(item[1].strip())
            new_hub_name = list(new_hub.keys())[0]
            existing_names = [list(h.keys())[0] for h in cfg.hubs]

            if new_hub_name in existing_names:
                raise ConfigError(
                    error(f'''Hub named "{new_hub_name}" already exists.''')
                )

            cfg.hubs.append(new_hub)

            if item[0] == "end_hub":
                hub_ended = True

        elif item[0] == "connection" and hub_started and hub_ended:
            cfg.connections.append(to_connection(item[1].strip()))

        else:
            raise ConfigError(
                f"\n{comment('# Configuration file expected structure:')}\n"
                "\nnb_drones: NB_DRONES"
                "\nstart_hub: NAME X Y [OPTIONAL_CRITERIA]"
                "\nhub: NAME X Y [OPTIONAL_CRITERIA]"
                "\n[...]"
                "\nend_hub: NAME X Y [OPTIONAL_CRITERIA]"
                "\nconnection: NAME-NAME [OPTIONAL_CRITERIA]"
                "\n[...]\n"
                f"\n{comment('# Hub OPTIONAL_CRITERIA: ')}"
                f"{comment('[zone=ZONE color=COLOR max_drones=MAX_DRONES]')}"
                f"\n{comment('# Connection OPTIONAL_CRITERIA: ')}"
                f"{comment('[max_link_capacity=MAX_LINK_CAPACITY]')}"
                )

    return (cfg)
