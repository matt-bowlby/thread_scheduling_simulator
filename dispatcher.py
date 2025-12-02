from thread_handling.thread import Thread
from algorithms import Algorithm


class Dispatcher:
    """
    Manages the scheduling and execution of threads using a specified algorithm.
    """

    def __init__(self, threads: list[Thread], algorithm: Algorithm) -> None:
        self.time_step: int = 0  # Current time step of the simulation
        self.threads: list[Thread] = threads  # All threads to be scheduled
        self.algorithm: Algorithm = algorithm  # Scheduling algorithm to use
        self.gantt_chart: list[tuple[str, int]] = []  # List to store Gantt chart data

    def tick(self) -> None:
        """Advances the simulation by one time step."""
        # Get currently active thread from the algorithm
        current_thread = self.algorithm.tick(self.threads, self.time_step)

        # Log the current thread in the Gantt chart
        if current_thread:
            print(f"Time {self.time_step}: Running Thread {current_thread.thread_id}")
            self.gantt_chart.append((current_thread.thread_id, self.time_step))
        # If no thread is active, log idle time
        else:
            print(f"Time {self.time_step}: CPU IDLE")
            self.gantt_chart.append(("IDLE", self.time_step))

        # Advance time step
        self.time_step += 1

    def reset(self) -> None:
        """Resets the dispatcher and all threads for a new simulation."""
        self.time_step = 0
        self.algorithm.reset()
        for thread in self.threads:
            thread.reset()

    def is_finished(self) -> bool:
        """Checks if all threads have finished execution."""
        return all(th.is_finished() for th in self.threads)
