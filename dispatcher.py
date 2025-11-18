from thread import Thread
from collections import deque
from algorithms import Algorithm

class Dispatcher:
	def __init__(self, threads: list[Thread], algorithm: Algorithm):
		self.time_step: int = 0
		self.threads: list[Thread] = threads
		self.algorithm: Algorithm = algorithm
		self.gantt_chart: list[tuple[str,int]] = [] # store tuples representing who ran at each time unit

	def add_thread(self, thread: Thread):
		self.threads.append(thread)

	def tick(self):
		for th in self.threads:
			if th.arrival == self.time_step:
				self.algorithm.threads.append(th)
		# Add newly arrived threads to the ready queue
		current_thread = self.algorithm.tick(self.time_step)
		# print(current_thread)
		if current_thread:
			print(f"Time {self.time_step}: Running Thread {current_thread.thread_id}")
			self.gantt_chart.append((current_thread.thread_id, self.time_step))

		self.time_step += 1

	def reset(self) -> None:
		self.time_step = 0
		for thread in self.threads:
			thread.reset()
