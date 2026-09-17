from .config import ConfigError


def to_connection(config: str) -> tuple[str, str]:

    info = config.split("-")
    if len(info) != 2:
        raise ConfigError("expected BLA BLA BLA, got not BLA BLA BLA")

    return (info[0], info[1])


def compare_connections(con: tuple[str, str]) -> bool:
    return True
