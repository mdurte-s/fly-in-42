from ..utils import bold


class SimulationError(Exception):
    """ Raised when the simulation fails to complete. """

    def __init__(self, message: str = bold("[Simulation Error]")) -> None:
        """ Initialize the exception with a message."""
        super().__init__(message)


class PathFindingError(SimulationError):
    """ Raised when the path is invalid. """

    def __init__(self, message: str = "PathFinding Error") -> None:
        """ Initialize the exception with a message. """
        super().__init__(message)
