from typing import Optional, TYPE_CHECKING
from .hub import Hub
from .connection import Connection

if TYPE_CHECKING:
    from ..parsing.config import Config


class Graph():

    def __init__(self) -> None:
        self._hubs: dict[str, Hub] = {}
        self._connections: list[Connection] = []
        self._start_hub: Optional[Hub] = None
        self._end_hub: Optional[Hub] = None

    @classmethod
    def from_config(cls, cfg: Config) -> "Graph":
        """ Factory method to build a Graph from a parsed Config object. """
        graph = cls()

        for i, hub in enumerate(cfg.hubs):
            is_start = i == 0
            is_end = i == len(cfg.hubs) - 1
            graph.add_hub(hub, is_start, is_end)

        for connection in cfg.connections:
            graph.add_connection(connection)

        return graph

    def add_hub(
            self, hub: Hub, is_start: bool = False,
            is_end: bool = False
            ) -> None:
        self._hubs[hub.name] = hub
        self._start_hub = hub if is_start else None
        self._end_hub = hub if is_end else None

    def add_connection(self, connection: Connection) -> None:
        self._connections.append(connection)

    @property
    def hubs(self) -> dict[str, Hub]:
        return self._hubs

    @property
    def connections(self) -> list[Connection]:
        return self._connections

    @property
    def start_hub(self) -> Optional[Hub]:
        return self._start_hub

    @property
    def end_hub(self) -> Optional[Hub]:
        return self._end_hub
