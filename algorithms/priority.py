from .algorithm import Algorithm
from thread_handling.thread import Thread


class Priority(Algorithm):
    def tick(self, threads: list[Thread], time_step: int) -> Thread | None:
        """
        Preemptive Priority Scheduling Algorithm
        Pick the highest-priority (lowest number) thread that has arrived.
        If a new higher-priority thread arrives, preempt the current active thread.
        """
        # Gather all threads that have arrived and not finished
        available = [
            th for th in threads if th.arrival <= time_step and not th.is_finished()
        ]
        if not available:
            # no threads available to run this tick
            self.active_thread = None
            return None

        # Choose best thread based on priority, then arrival time
        highest_priority_thread = min(
            available, key=lambda th: (th.priority, th.arrival)
        )

        # Preempt if needed
        if (
            self.active_thread is None
            or self.active_thread.is_finished()
            or highest_priority_thread.priority < self.active_thread.priority
        ):
            self.active_thread = highest_priority_thread

        # Run active thread for one tick
        self.active_thread.tick(time_step)
        return self.active_thread
