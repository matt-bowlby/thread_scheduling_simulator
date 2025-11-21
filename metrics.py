from thread import Thread

def calculate_metrics(threads: list[Thread], total_time: int) -> dict:
    '''
    Computes summary performance metircs for teh scheduling simulation
    Args: 
    threads: List of completed thread objects
    total_time: Total simulation time (in ticks)
    Returns:
    dict: containing the average waiting time, average turnarround time, 
     CPU utilization, and throughput.
    '''
    n = len(threads)

    # Average Waiting Time
    avg_waiting = sum(th.waiting_time for th in threads) / n

    # Average Turnaround Time
    avg_turnaround = sum(th.turnaround_time for th in threads) / n

    # CPU Utilization = (Time CPU busy(which is sum of all bursts) / Total simulation time
    busy_time = sum(th.burst for th in threads)
    cpu_utilization = busy_time / total_time if total_time > 0 else 0

    # Throughput = completed threads / total simulation time
    throughput = n/ total_time if total_time > 0 else 0

    return {
        "average_waiting_time" : avg_waiting, 
        "average_turnaround_time" : avg_turnaround, 
        "cpu_utilization" : cpu_utilization, 
        "throughput" : throughput, 
        "total_time": total_time
    }
    