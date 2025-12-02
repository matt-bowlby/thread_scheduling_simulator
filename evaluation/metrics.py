from thread_handling.thread import Thread


def calculate_metrics(
    threads: list[Thread], gantt_chart: list[tuple[str, int]]
) -> dict:
    """
    Calculate key performance metrics based on the completed threads and Gantt chart data.
    1. Average Waiting Time
    2. Average Turnaround Time
    3. CPU Utilization
    4. Throughput
    5. Total Time
    """
    n = len(threads)

    # Computing the total simulation time
    total_time = len(gantt_chart)

    # CPU busy_time = count the number of ticks where CPU was NOT IDLE
    busy_time = sum(1 for tid, _ in gantt_chart if tid != "IDLE")

    # Average waiting time
    avg_waiting = sum(th.waiting_time for th in threads) / n if n > 0 else 0

    # Average turnaround time
    avg_turnaround = sum(th.turnaround_time for th in threads) / n if n > 0 else 0

    # CPU Utilization (percentage) = (Time CPU busy (i.e., sum of busy ticks) / Total simulation time)
    cpu_utilization = (busy_time / total_time * 100) if total_time > 0 else 0

    # Throughput = completed threads / total simulation time
    throughput = (n / total_time) if total_time > 0 else 0

    return {
        "average_waiting_time": avg_waiting,
        "average_turnaround_time": avg_turnaround,
        "cpu_utilization": cpu_utilization,
        "throughput": throughput,
        "total_time": total_time,
    }
