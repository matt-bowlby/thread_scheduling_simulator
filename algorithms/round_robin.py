from collections import deque
from .algorithm import Algorithm
from thread import Thread

class RR(Algorithm):
	def __init__(self, threads: list[Thread], quantum: int) -> None:
		super().__init__(threads)
		self.quantum = quantum
		self.ready_queue = deque()
		self.active_thread: Thread | None = None
		self.time_used = 0# how long the active thread has used the CPU in the current quantum

	def tick(self, time_step: int) -> Thread | None:
		'''
		RR adds amew;y arrived threads to ready queue
		If active thread finsihed or quantum expired -> rotate
		Run active thread for onw tick
		'''
		# Add newly arrived threads to ready queue
		# for th in self.threads:
		pass