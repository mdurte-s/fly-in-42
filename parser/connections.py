from .config import ConfigError, StructError, connection
from .utils import to_int, comment, error, m_error


def hub_exists(name: str, hub_names: list[str]) -> bool:
    return name in hub_names


def to_connection(config: str, hub_names: list[str]) -> tuple[str, str, int]:

    info = config.split()
    if not info or len(info) > 2:
        raise StructError(error(connection))

    max_link = (to_int(info[1], 1, True) if len(info) == 2 else -1)

    con = info[0].split("-")
    if len(con) != 2:
        raise StructError(error(connection))

    for c in con:
        if not hub_exists(c, hub_names):
            raise ConfigError(
                m_error(f"'{c}' hub is not defined.") +
                comment("\nDefined Hubs:") +
                comment(f"\n{(", ").join(hub_names)}"))

    return (con[0], con[1], max_link)
