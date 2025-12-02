from thread_handling.thread import Thread


class Algorithm:
    """
    Base class for all scheduling algorithms.
    """

    def __init__(self) -> None:
        self.active_thread: Thread | None = None

    def tick(self, threads: list[Thread], time_step: int) -> Thread | None:
        """
        Runs the algorithm for the current tick and returns the currently active thread.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def reset(self):
        """
        Resets the algorithm state for a new simulation.
        """
        self.active_thread = None
