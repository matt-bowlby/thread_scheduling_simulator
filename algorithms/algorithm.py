from thread import Thread

class Algorithm:
	def __init__(self, threads: list[Thread]) -> None:
		self.threads = threads
		self.time_step = 0

	def tick(self, time_step: int) -> Thread | None:
		raise NotImplementedError("This method should be overridden by subclasses")