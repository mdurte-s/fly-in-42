import heapq
from typing import Optional
from ..models.hub import Hub
from ..models.connection import Connection


class PathFinder:
    """ Calculates best paths in the graph for drone distribution. """

    def __init__(self, hubs: list[Hub], connections: list[Connection]) -> None:
        """Initialize PathFinder with available hubs and connections.

        Args:
            hubs (list[Hub]): List of all network hubs.
            connections (list[Connection]): List of bidirectional connections.
        """
        self._hubs: dict[str, Hub] = {h.name: h for h in hubs}
        self._connections: list[Connection] = connections
        self._adj: dict[str, list[tuple[str, int, Connection]]] = {
            h.name: [] for h in hubs
        }
        self._build_adjacency_list()

    def _build_adjacency_list(self) -> None:
        """Build bidirectional adjacency list filtering out blocked zones."""
        for c in self._connections:
            h1, h2 = c.hub1, c.hub2

            if h2.zone != "blocked":
                self._adj[h1.name].append((h2.name, h2.cost, c))

            if h1.zone != "blocked":
                self._adj[h2.name].append((h1.name, h1.cost, c))

    def find_paths(
            self, start_name: str, end_name: str, max_paths: int
            ) -> list[list[Hub]]:
        """Find multiple candidate paths using Dijkstra with iterativ
        penalties.

        Args:
            start_name (str): Identifier of starting hub.
            end_name (str): Identifier of destination hub.
            max_paths (int): Maximum number of candidate paths to find.

        Returns:
            list[list[Hub]]: List of found paths from start to end.
        """
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
        """Calculate the shortest paths using lowest weighted cost and node
        penalties.

        Args:
            start_name (str): Start hub name.
            end_name (str): Destination hub name.
            penalties (dict[str, float]): Dynamic node penalties to encourage
            alternate routes.

        Returns:
            list[Hub]: Shortest path as ordered list of Hubs, or empty list if
            unreachable.
        """

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
