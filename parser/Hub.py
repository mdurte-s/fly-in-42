from dataclasses import dataclass


@dataclass
class Hub():

    hub = ("Expected: 'hub: "
           "NAME X Y [zone=ZONE color=COLOR max_drones=MAX_DRONES]'")

    def __init__(self,
                 name: str,
                 x: int,
                 y: int,
                 zone: str = "",
                 color: str = "",
                 max_drones: int = 0) -> None:

        self._name: str = name
        self._x: int = x
        self._y: int = y
        self._zone: str = zone
        self._color: str = color
        self._max_drones: int = max_drones
