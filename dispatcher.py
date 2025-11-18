from thread import Thread

class Dispatcher:
	def __init__(self, threads: list[Thread], quantum: int = 2):
		self.time_step: int = 0
		self.threads: list[Thread] = threads
		self.quantum: int = quantum  # Default quantum time

	def add_thread(self, thread: Thread):
		self.threads.append(thread)

	def tick(self):
		self.time_step += 1

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
