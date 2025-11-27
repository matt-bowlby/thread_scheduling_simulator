from thread import Thread

class Algorithm:
	def __init__(self) -> None:
		self.active_thread: Thread | None = None
		self.time_step = 0

	def tick(self, threads: list[Thread], time_step: int) -> Thread | None:
		raise NotImplementedError("This method should be overridden by subclasses")

	def reset(self):
		self.active_thread = None
		self.time_step = 0