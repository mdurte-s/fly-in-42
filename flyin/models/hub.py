from dataclasses import dataclass
from typing import Optional


@dataclass
class Hub():

    EXPECTED_FORMAT = (
        "Expected: 'hub: "
        "NAME X Y [zone=ZONE color=COLOR max_drones=MAX_DRONES]'")

    def __init__(
            self, name: str, x: int, y: int, zone: str = "normal",
            color: str = "", max_drones: int = 1
            ) -> None:

        self._name: str = name
        self._x: int = x
        self._y: int = y
        self._zone: str = zone
        self._color: str = color
        self._max_drones: int = max_drones
        self._visited: bool = False
        self._previous: Optional[Hub] = None
        self._cost: int = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def coordinates(self) -> tuple[int, int]:
        return (self._x, self._y)

    @property
    def zone(self) -> str:
        return self._zone

    @property
    def max_drones(self) -> int:
        return self._max_drones
