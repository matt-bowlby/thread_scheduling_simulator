from .algorithm import Algorithm
from thread_handling.thread import Thread


class FCFS(Algorithm):
    def tick(self, threads: list[Thread], time_step: int) -> Thread | None:
        """
        Runs the FCFS scheduling algorithm for the current tick. FCFS selects the thread that arrived first among the available threads.
        """

        # If there's no active thread or the active thread is finished, pick next thread.
        if self.active_thread is None or self.active_thread.is_finished():
            # Get all non-finished threads
            available = [
                t for t in threads if (not t.is_finished()) and (t.arrival <= time_step)
            ]
            # If no available threads, return None
            if not available:
                return None
            # Pick the one with the earliest arrival time
            self.active_thread = min(available, key=lambda t: t.arrival)

        # Tick the active thread
        self.active_thread.tick(time_step)

        # Return the active thread
        return self.active_thread
