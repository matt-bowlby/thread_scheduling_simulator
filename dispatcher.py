from thread import Thread
from collections import deque

class Dispatcher:
	def __init__(self, threads: list[Thread], quantum: int = 2):
		self.time_step: int = 0
		self.threads: list[Thread] = threads
		self.quantum: int = quantum  # Default quantum time
		self.ready_queue: deque[Thread] = deque() # Holds Thread objects that have arrived and are waiting to run
		self.gantt_chart: list[tuple[str,int]] = [] # store tuples representing who ran at each time unit

	def add_thread(self, thread: Thread):
		self.threads.append(thread)

	def tick(self):
		self.time_step += 1
		# Add newly arrived threads to the ready queue
		for th in self.threads: 
			if th.arrival == self.time_step:
				self.ready_queue.append(th)

	def reset(self) -> None:
		self.time_step = 0
		for thread in self.threads:
			thread.reset()

	def get_next_thread(self) -> Thread | None:
		# Simple FCFS scheduling for demonstration
		available_threads = [t for t in self.threads if t.arrival <= self.time_step and not t.is_finished()]
		if not available_threads:
			return None
		return min(available_threads, key=lambda t: t.arrival)
