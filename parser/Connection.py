from dataclasses import dataclass


@dataclass
class Connection():

    connection = ("Expected: 'connection: "
                  "NAME-NAME [max_link_capacity=MAX_LINK_CAPACITY]'")

    def __init__(self,
                 hub1: str,
                 hub2: str,
                 max_link_capacity: int) -> None:

        self._hub1: str = hub1
        self._hub2: int = hub2
        self._max_link_capacity: int = max_link_capacity
