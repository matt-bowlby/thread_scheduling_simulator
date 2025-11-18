from .algorithm import Algorithm
from thread import Thread

class Priority(Algorithm):
	def __init__(self, threads: list[Thread]) -> None:
		super().__init__(threads)

	def tick(self, time_step: int) -> Thread | None:
		pass