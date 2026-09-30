from typing import Optional
from .hub import Hub
from .connection import Connection


class Graph():

    def __init__(self) -> None:
        self._hubs: dict[str, Hub] = {}
        self._connections: list[Connection] = []
        self._start_hub: Optional[Hub] = None
        self._end_hub: Optional[Hub] = None

    def add_hub(self,
                hub: Hub,
                is_start: bool = False,
                is_end: bool = False
                ) -> None:
        self._hubs[hub.name] = hub
        if is_start:
            self._start_hub = hub
        if is_end:
            self._end_hub = hub

    def add_connection(self, connection: Connection) -> None:
        self._connections.append(connection)

    @property
    def start_hub(self) -> Optional[Hub]:
        return self._start_hub

    @property
    def end_hub(self) -> Optional[Hub]:
        return self._end_hub
