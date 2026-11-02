from dataclasses import dataclass
from typing import Optional


@dataclass
class Hub():
    """Represents a network zone / hub with coordinates and capacity rules."""

    EXPECTED_FORMAT = (
        "Expected: 'hub: "
        "NAME X Y [zone=ZONE color=COLOR max_drones=MAX_DRONES]'"
    )

    def __init__(
            self, name: str, x: int, y: int, zone: str = "normal",
            color: str = "", max_drones: int = 1
            ) -> None:
        """Initialize a Hub zone.

        Args:
            name (str): Unique identifier name without spaces or dashes.
            x (int): X Cartesian coordinate.
            y (int): Y Cartesian coordinate.
            zone (str): Zone type ('normal', 'restricted', 'priority',
            'blocked').
            color (str): Color name for visualization.
            max_drones (int): Maximum simultaneous drone capacity.
        """
        self._name: str = name
        self._x: int = x
        self._y: int = y
        self._zone: str = zone
        self._color: str = color
        self._max_drones: int = max_drones
        self._visited: bool = False
        self._previous: Optional[Hub] = None
        self._occupancy: int = 0
        self._spots_reserved: int = 0

    @property
    def name(self) -> str:
        """Return the hub name."""
        return self._name

    @property
    def coordinates(self) -> tuple[int, int]:
        """Return (X, Y) integer coordinates."""
        return (self._x, self._y)

    @property
    def zone(self) -> str:
        """Return the zone classification type."""
        return self._zone

    @property
    def color(self) -> str:
        """Return the visual representation color."""
        return self._color

    @property
    def max_drones(self) -> int:
        """Return the maximum allowed drone capacity."""
        return self._max_drones

    @property
    def cost(self) -> int:
        """Return movement turn cost to enter this zone
        (restricted=2, normal/priority=1).
        """
        if self._zone == "restricted":
            return 2
        elif self._zone == "blocked":
            return 0
        else:
            return 1

    @property
    def occupancy(self) -> int:
        """Return current number of drones occupying in this zone.
        """
        return self._occupancy

    @property
    def spots_reserved(self) -> int:
        """Return current number of spots reserved in this zone.
        """
        return self._spots_reserved

    def increase_occupancy(self, occupancy: int = 1) -> None:
        """Increase the occupancy counter for the current hub.

        Args:
            occupancy (int): Usage increment amount (default: 1).
        """
        self._occupancy += occupancy

    def decrease_occupancy(self, occupancy: int = 1) -> None:
        """Decrease the occupancy counter for the current hub.

        Args:
            occupancy (int): Usage decrement amount (default: 1).
        """
        self._occupancy -= occupancy

    def increase_spots_reserved(self, spots_reserved: int = 1) -> None:
        """Increase the spots_reserved counter for the current hub.

        Args:
            spots_reserved (int): Usage increment amount (default: 1).
        """
        self._spots_reserved += spots_reserved

    def decrease_spots_reserved(self, spots_reserved: int = 1) -> None:
        """Decrease the spots_reserved counter for the current hub.

        Args:
            spots_reserved (int): Usage decrement amount (default: 1).
        """
        self._spots_reserved -= spots_reserved
