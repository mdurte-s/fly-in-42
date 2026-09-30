from dataclasses import dataclass
from .hub import Hub


@dataclass
class Connection():

    EXPECTED_FORMAT = (
        "Expected: 'connection: "
        "NAME-NAME [max_link_capacity=MAX_LINK_CAPACITY]'")

    def __init__(self,
                 hub1: Hub,
                 hub2: Hub,
                 max_link_capacity: int = 1) -> None:

        self._hub1: Hub = hub1
        self._hub2: Hub = hub2
        self._max_link_capacity: int = max_link_capacity

    @property
    def hub1(self) -> Hub:
        return self._hub1

    @property
    def hub2(self) -> Hub:
        return self._hub2

    @property
    def max_link_capacity(self) -> int:
        return self._max_link_capacity
