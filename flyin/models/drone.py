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

    @property
    def name(self) -> str:
        return self._name

    @property
    def current_hub(self) -> Hub:
        return self._current_hub

    @property
    def is_active(self) -> bool:
        return not self._arrived
