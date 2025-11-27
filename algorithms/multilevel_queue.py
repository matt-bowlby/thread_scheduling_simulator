from collections import deque
from .algorithm import Algorithm
from thread import Thread

class MultilevelQueue(Algorithm):
    def __init__(self, quantum: int) -> None:
        super().__init__()
        # Two queues: high priority (RR), low priority (FCFS)
        self.high_queue = deque() # RR queue (priority 1-2)
        self.low_queue = deque()  # FCFS queue (priority >= 3)
        self.quantum = quantum
        self.time_used = 0 # how long the active thread has used the CPU in the current quantum

    def _add_arrivals(self, threads: list[Thread], time_step : int):
        '''
        Move newly arrived thread to an appropiate queue'''
        for th in threads:
            if th.arrival == time_step:
                if th.priority <= 2:
                    self.high_queue.append(th)
                else:
                    self.low_queue.append(th)

    def tick(self, threads: list[Thread], time_step: int) -> Thread | None:
        '''
        Multilevel Queue Scheduling Algorithm
        High priority queue (priority 1-2) uses Round Robin
        Low priority queue (priority >=3) uses FCFS
        '''
        # Add newly arrived threads to appropiate queue
        self._add_arrivals(time_step)

        # IF active thre finished, clear it
        if self.active_thread and self.active_thread.is_finished():
            self.active_thread = None
            self.time_used = 0

        # Preemptive low priority thread if a high_priority one arrives
        if self.active_thread and self.active_thread.priority > 2:
            if self.high_queue:
                self.low_queue.append(self.active_thread)
                self.active_thread = None
                self.time_used = 0

        # Select from high queue
        if self.high_queue or (self.active_thread and self.active_thread.priority <= 2):

            #if no active thread, pick next from queue
            if self.active_thread is None:
                self.active_thread = self.high_queue.popleft()
                self.time_step = 0
            # if quantum has experied
            elif self.time_used >= self.quantum:
                # Requeue if not finished
                if not self.active_thread.is_finished():
                    self.high_queue.append(self.active_thread)
                # select next thread
                if self.high_queue:
                    self.active_thread = self.high_queue.popleft()
                else:
                    self.active_thread = None
                self.time_used = 0

        # Low queue
        else:
            if self.active_thread is None:
                if self.low_queue:
                    self.active_thread = self.low_queue.popleft()
                else:
                    return None

        # Tick the active thread
        if self.active_thread:
            self.active_thread.tick(time_step)
            # Count Quantum only for high priority threads
            if self.active_thread.priority <= 2:
                self.time_used += 1

        return self.active_thread

    def reset(self):
        super().reset()
        self.high_queue.clear()
        self.low_queue.clear()
        self.time_used = 0