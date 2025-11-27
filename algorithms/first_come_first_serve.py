from .algorithm import Algorithm
from thread import Thread

class FCFS(Algorithm):
	def tick(self, threads: list[Thread], time_step: int) -> Thread | None:
		'''
		FCFS picks the first thread based on arrival
		'''
		# If no active thread or active thread is finished, pick next
		if self.active_thread is None or self.active_thread.is_finished():
			# Get all non-finished threads
			available=[t for t in threads if (not t.is_finished()) and (t.arrival <= time_step)]
			# If no available threads, return
			if not available:
				return None
			# Pick the one with the earliest arrival time
			self.active_thread = min(available, key=lambda t: t.arrival)

		# Tick the active thread
		self.active_thread.tick(time_step)

		# Return the active thread
		return self.active_thread