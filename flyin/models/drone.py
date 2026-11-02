from dataclasses import dataclass
from typing import Optional
from .hub import Hub


@dataclass
class Drone():
    """Represents a simulated drone navigating the network of zones."""

    def __init__(self, id: int, start_hub: Hub) -> None:
        """Initialize a Drone instance.

        Args:
            id (int): Unique drone integer identifier.
            start_hub (Hub): The initial hub where the drone starts.
        """
        self._id: int = id
        self._name: str = f"D{id}"
        self._current_hub: Hub = start_hub
        self._in_transit_to: Optional[Hub] = None
        self._is_in_intermediate_transit: bool = False
        self._turns_remaining: int = 0
        self._turns_count: int = 0
        self._arrived: bool = False
        self._path_id: int = 0

    @property
    def name(self) -> str:
        """Return the unique drone identifier name (e.g. 'D1')."""
        return self._name

    @property
    def current_hub(self) -> Hub:
        """Return the current zone hub occupied by the drone."""
        return self._current_hub

    @property
    def in_transit_to(self) -> Hub | None:
        """Return destination zone if in multi-turn transit, else None."""
        return self._in_transit_to

    @property
    def is_in_intermediate_transit(self) -> bool:
        """Return True if the drone is currently mid-transit on a 2-turn
        movement.
        """
        return self._is_in_intermediate_transit

    @property
    def is_active(self) -> bool:
        """Return True if the drone has not yet reached the end zone."""
        return not self._arrived

    @property
    def turns_remaining(self) -> int:
        """Return remaining transit turns before reaching destination hub."""
        return self._turns_remaining

    @property
    def turns_count(self) -> int:
        """Return current turns count."""
        return self._turns_count

    @property
    def path_id(self) -> int:
        """Return the assigned candidate path index for this drone."""
        return self._path_id

    def set_current_hub(self, current_hub: Hub) -> None:
        """Update the drone's current hub location.

        Args:
            current_hub (Hub): New hub location.
        """
        self._current_hub = current_hub

    def set_in_transit_to(self, in_transit_to: Hub | None) -> None:
        """Set the destination hub during transit.

        Args:
            in_transit_to (Hub | None): Destination hub or None.
        """
        self._in_transit_to = in_transit_to

    def set_in_intermediate_transit(self, state: bool) -> None:
        """Set whether the drone is in the first leg of a multi-turn transit.
        """
        self._is_in_intermediate_transit = state

    def set_turns_remaining(self, turns_remaining: int) -> None:
        """Set the number of turns remaining in transit.

        Args:
            turns_remaining (int): Number of turns left.
        """
        self._turns_remaining = turns_remaining

    def increase_turns_count(self, turns: int = 1) -> None:
        """Increase the turns counter for the current drone.

        Args:
            turns (int): Usage increment amount (default: 1).
        """
        self._turns_count += turns

    def set_arrived(self, arrived: bool) -> None:
        """Mark whether the drone has reached the end zone.

        Args:
            arrived (bool): True if arrived at destination.
        """
        self._arrived = arrived

    def set_path_id(self, path_id: int) -> None:
        """Assign a path index to this drone.

        Args:
            path_id (int): Index of path in candidate paths list.
        """
        self._path_id = path_id
