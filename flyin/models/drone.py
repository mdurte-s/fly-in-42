from dataclasses import dataclass
from typing import Optional
from .hub import Hub


@dataclass
class Drone():

    def __init__(self, id: int, start_hub: Hub) -> None:
        self._id: int = id
        self._name: str = f"D{id}"
        self._current_hub: Hub = start_hub
        self._in_transit_to: Optional[Hub] = None
        self._turns_remaining: int = 0
        self._arrived: bool = False
        self._path_id: int = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def current_hub(self) -> Hub:
        return self._current_hub

    @property
    def in_transit_to(self) -> Hub:
        return self._in_transit_to

    @property
    def is_active(self) -> bool:
        return not self._arrived

    @property
    def turns_remaining(self) -> int:
        return self._turns_remaining

    @property
    def path_id(self) -> int:
        return self._path_id

    def set_current_hub(self, current_hub: Hub) -> None:
        self._current_hub = current_hub

    def set_in_transit_to(self, in_transit_to: Hub) -> None:
        self._in_transit_to = in_transit_to

    def set_turns_remaining(self, turns_remaining: int) -> None:
        self._turns_remaining = turns_remaining

    def set_arrived(self, arrived: bool) -> None:
        self._arrived = arrived

    def set_path_id(self, path_id: int) -> None:
        self._path_id = path_id
