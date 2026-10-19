from typing import Optional, TYPE_CHECKING
from .hub import Hub
from .connection import Connection

if TYPE_CHECKING:
    from ..parsing.config import Config


class Graph():
    """Graph structure representing the network of hubs and connections."""

    def __init__(self) -> None:
        """Initialize an empty Graph."""
        self._hubs: dict[str, Hub] = {}
        self._connections: list[Connection] = []
        self._start_hub: Optional[Hub] = None
        self._end_hub: Optional[Hub] = None

    @classmethod
    def from_config(cls, cfg: Config) -> "Graph":
        """Factory method to build a Graph from a parsed Config object.

        Args:
            cfg (Config): Parsed configuration instance.

        Returns:
            Graph: Populated graph containing hubs and connections.
        """
        graph = cls()

        for hub in cfg.hubs:
            is_start = (cfg.start_hub is not None and
                        hub.name == cfg.start_hub.name)
            is_end = (cfg.end_hub is not None and
                      hub.name == cfg.end_hub.name)
            graph.add_hub(hub, is_start, is_end)

        for connection in cfg.connections:
            graph.add_connection(connection)

        return graph

    def add_hub(
            self, hub: Hub, is_start: bool = False,
            is_end: bool = False
            ) -> None:
        """Add a hub to the graph.

        Args:
            hub (Hub): The hub instance to add.
            is_start (bool): True if this hub is the starting zone.
            is_end (bool): True if this hub is the end destination zone.
        """
        self._hubs[hub.name] = hub
        if is_start:
            self._start_hub = hub
        if is_end:
            self._end_hub = hub

    def add_connection(self, connection: Connection) -> None:
        """Add a connection edge to the graph.

        Args:
            connection (Connection): Connection edge to add.
        """
        self._connections.append(connection)

    @property
    def hubs(self) -> dict[str, Hub]:
        """Return dictionary mapping hub names to Hub instances."""
        return self._hubs

    @property
    def connections(self) -> list[Connection]:
        """Return list of all connections in the graph."""
        return self._connections

    @property
    def start_hub(self) -> Optional[Hub]:
        """Return the start hub instance if set, else None."""
        return self._start_hub

    @property
    def end_hub(self) -> Optional[Hub]:
        """Return the end hub instance if set, else None."""
        return self._end_hub
