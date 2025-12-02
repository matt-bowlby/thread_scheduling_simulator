import random
from .thread import Thread


def generate_threads(
    num_threads: int,
    max_arrival_time: int = 100,
    burst_time_range: tuple[int, int] = (1, 10),
    priority_range: tuple[int, int] = (0, 10),
) -> list[Thread]:
    """Generates a list of random threads based on the specified parameters."""
    threads = []
    for i in range(num_threads):
        arrival_time = random.randint(0, max_arrival_time)
        burst_time = random.randint(*burst_time_range)
        priority = random.randint(*priority_range)
        threads.append(Thread(f"T{i}", arrival_time, burst_time, priority))
    return threads
