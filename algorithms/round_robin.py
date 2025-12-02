from collections import deque
from .algorithm import Algorithm
from thread_handling.thread import Thread


class RR(Algorithm):
    def __init__(self, quantum: int) -> None:
        super().__init__()
        self.quantum = quantum
        self.ready_queue = deque()
        self.time_used = (
            0  # how long the active thread has used the CPU in the current quantum
        )

    def tick(self, threads: list[Thread], time_step: int) -> Thread | None:
        """
        RR adds newly arrived threads to the ready queue.
        If the active thread finished or the quantum expired -> rotate.
        Run the active thread for one tick.
        """
        # Add newly arrived threads to ready queue
        for th in threads:
            if th.arrival == time_step:
                self.ready_queue.append(th)

        # If there is no active thread or it finished, get next thread from queue
        if self.active_thread is None or self.active_thread.is_finished():
            if self.active_thread and self.active_thread.is_finished():
                pass  # finished thread, do not re-add to queue
            # picking next thread
            if self.ready_queue:
                self.active_thread = self.ready_queue.popleft()
                self.time_used = 0
            else:
                return None

        # If quantum expired, rotate
        if self.time_used >= self.quantum:
            # Put active thread back to queue if not finished
            if not self.active_thread.is_finished():
                self.ready_queue.append(self.active_thread)
            # Pick next thread
            if self.ready_queue:
                self.active_thread = self.ready_queue.popleft()

            self.time_used = 0

        # Run active thread for one tick
        self.active_thread.tick(time_step)
        self.time_used += 1
        return self.active_thread

    def reset(self):
        super().reset()
        self.ready_queue.clear()
        self.time_used = 0
