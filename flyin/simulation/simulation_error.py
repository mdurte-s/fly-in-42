from ..utils import error


class SimulationError(Exception):
    """ Raised when the simulation fails to complete. """

    def __init__(
            self, message: str = error("Unexpected Simulation Failure.")
            ) -> None:
        """ Initialize the exception with a message."""
        super().__init__(message)


class PathFindingError(SimulationError):
    """ Raised when the path is invalid. """

    def __init__(
            self, message: str = error("Unexpected Path Finding Failure.")
            ) -> None:
        """ Initialize the exception with a message. """
        super().__init__(message)
