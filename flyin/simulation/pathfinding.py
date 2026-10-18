import heapq
from typing import Optional
from ..models.hub import Hub
from ..models.connection import Connection


class PathFinder:
    """ Calculates best paths in the graph for drone distribution. """

    def __init__(self, hubs: list[Hub], connections: list[Connection]) -> None:

        self._hubs: dict[str, Hub] = {h.name: h for h in hubs}
        self._connections: list[Connection] = connections
        self._adj: dict[str, list[tuple[str, int, Connection]]] = {
            h.name: [] for h in hubs
        }
        self._build_adjacency_list()

    def _build_adjacency_list(self) -> None:
        for c in self._connections:
            h1, h2 = c.hub1, c.hub2

            if h2.zone != "blocked":
                cost2 = 2 if h2.zone == "restricted" else 1
                self._adj[h1.name].append((h2.name, cost2, c))

            if h1.zone != "blocked":
                cost1 = 2 if h1.zone == "restricted" else 1
                self._adj[h2.name].append((h1.name, cost1, c))

    def find_paths(
            self, start_name: str, end_name: str, max_paths: int
            ) -> list[list[Hub]]:
        """ Find multiple candidate paths using Dijkstra algorithm """

        penalties: dict[str, float] = {h: 0.0 for h in self._hubs}
        paths: list[list[Hub]] = []
        for _ in range(max_paths):
            path = self.dijkstra(start_name, end_name, penalties)
            if not path:
                break
            paths.append(path)
            for hub in path[1:-1]:
                penalties[hub.name] += 5.0

        return paths

    def dijkstra(
            self, start_name: str, end_name: str, penalties: dict[str, float]
            ) -> list[Hub]:
        """ Calculates the shortest path considering the lowest weighted cost
        and penalties. """

        distances: dict[str, float] = {h: float('inf') for h in self._hubs}
        previous: dict[str, Optional[str]] = {h: None for h in self._hubs}

        distances[start_name] = 0
        pq: list[tuple[float, str]] = [(0, start_name)]

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_dist > distances[current_node]:
                continue

            if current_node == end_name:
                break

            for neighbor, cost, _ in self._adj[current_node]:
                weight = float(cost)
                if self._hubs[neighbor].zone == "priority":
                    weight *= 0.9
                penalty = penalties.get(neighbor, 0.0)
                all_weight = weight + penalty
                if distances[current_node] + all_weight < distances[neighbor]:
                    distances[neighbor] = distances[current_node] + all_weight
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distances[neighbor], neighbor))

        path: list[Hub] = []
        curr: Optional[str] = end_name
        while curr is not None:
            path.append(self._hubs[curr])
            curr = previous[curr]
        path.reverse()

        return path if path[0].name == start_name else []
