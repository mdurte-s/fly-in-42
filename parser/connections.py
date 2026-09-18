from .config import StructError, connection
from .utils import to_int, error

# falta verificar
# - se os nomes das zonas existem;
# - e que o start e o goal tem connects;


def to_connection(config: str) -> tuple[str, str, int]:

    info = config.split()
    if len(info) > 2:
        raise StructError(error(connection))

    con = info[0].split("-")

    if len(con) != 2:
        raise StructError(error(connection))

    if len(info) == 2:
        return (con[0], con[1], to_int(info[1], 1, True))

    if len(info) == 1:
        return (con[0], con[1], 0)
