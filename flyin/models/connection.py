from dataclasses import dataclass
from .hub import Hub


@dataclass
class Connection():
    """Represents a bidirectional edge between two hubs with capacity.
    """

    EXPECTED_FORMAT = (
        "Expected: 'connection: "
        "NAME-NAME [max_link_capacity=MAX_LINK_CAPACITY]'"
        )

    def __init__(
            self, id: int, hub1: Hub, hub2: Hub, max_link_capacity: int = 1
            ) -> None:
        """Initialize a Connection between two hubs.

        Args:
            id (int): Unique connection integer identifier.
            hub1 (Hub): First endpoint hub.
            hub2 (Hub): Second endpoint hub.
            max_link_capacity (int): Maximum simultaneous traversing drones.
        """
        self._id: int = id
        self._hub1: Hub = hub1
        self._hub2: Hub = hub2
        self._max_link_capacity: int = max_link_capacity
        self._link_capacity: int = 0

    @property
    def id(self) -> int:
        """Return unique connection ID."""
        return self._id

    @property
    def hub1(self) -> Hub:
        """Return the first connected hub."""
        return self._hub1

    @property
    def hub2(self) -> Hub:
        """Return the second connected hub."""
        return self._hub2

    @property
    def max_link_capacity(self) -> int:
        """Return the maximum link capacity."""
        return self._max_link_capacity

    @property
    def link_capacity(self) -> int:
        """Return the current number of drones using this link this turn."""
        return self._link_capacity

    def increase_link(self, increament: int = 1) -> None:
        """Increase the link usage counter for the current turn.

        Args:
            increament (int): Usage increment amount (default: 1).
        """
        self._link_capacity += increament

    def reset_link(self) -> None:
        """Reset the link usage counter at the start of a turn."""
        self._link_capacity = 0
