from ..models import Hub
from ..parsing import Config
from ..utils import utils

# Each movement between zones has a cost in turns, based on the zone=type
# of the destination:
#   • normal: 1 turn (default)
#   • restricted: 2 turns
#   • priority: 1 turn (but should be preferred in pathfinding algorithms)
#   • blocked: Inaccessible — cannot be entered


class Simulation():

    def __init__(self,
                 cfg: Config,
                 path: list[Hub] = [],
                 nb_turns: int = 0
                 ) -> None:

        self._cfg: Config = cfg
        self._path: list[Hub] = path
        self._nb_turns = nb_turns

    def solver(self) -> None:

        self.find_previous()
        self.find_path(self._cfg._hubs[-1])

    def find_path(self, hub: Hub) -> None:

        if isinstance(hub, Hub):
            self._path.append(hub)
            if hub._name == self._cfg._hubs[0]._name:
                self._path.reverse()
                return
            return self.find_path(hub._previous)
        else:
            print(type(hub))
            print(utils.error("caput"))

    def find_previous(self) -> None:

        hubs = list(reversed(self._cfg._hubs))
        for hub in hubs:
            valid_connections = self.find_connections(hub)
            hub._visited = True
            for c in valid_connections:
                if not c._visited:
                    cost = 2 if c._zone == "restricted" else 1
                    if cost < hub._cost:
                        hub._previous = c
                        hub._cost = cost

    def find_connections(self, hub: Hub) -> list[Hub]:

        valid_connections: list[Hub] = []
        for c in self._cfg._connections:
            if c._hub1 is hub:
                valid_connections.append(c._hub2)
            elif c._hub2 is hub:
                valid_connections.append(c._hub1)
        return valid_connections

    def turns_count(self, zone: int) -> None:
        if zone == 1:
            self._nb_turns += 1
        elif zone == 2:
            self._nb_turns += 2
