"""
Test all algorithms with random threads and validate correctness
"""

from algorithms.first_come_first_serve import FCFS
from algorithms.shortest_job_first import SJF
from algorithms.priority import Priority
from algorithms.round_robin import RR
from algorithms.preemptive_shortest_job_first import PreemptiveSJF
from algorithms.multilevel_queue import MultilevelQueue
from dispatcher import Dispatcher
from thread_handling.thread import Thread
from evaluation.metrics import calculate_metrics
from thread_handling.thread_generator import generate_threads
import random


def validate_results(threads, gantt_chart, algorithm_name):
    """Validate the correctness of scheduling results"""
    errors = []

    # Check 1: All threads completed
    for thread in threads:
        if not thread.is_finished():
            errors.append(f"Thread {thread.thread_id} did not complete")
        if thread.completion_time == -1:
            errors.append(f"Thread {thread.thread_id} has no completion time")

    # Check 2: Total execution time matches burst times
    total_burst = sum(t.burst for t in threads)
    cpu_time = sum(1 for tid, _ in gantt_chart if tid != "IDLE")
    if cpu_time != total_burst:
        errors.append(f"CPU time ({cpu_time}) != Total burst time ({total_burst})")

    # Check 3: Turnaround time >= burst time for all threads
    for thread in threads:
        if thread.turnaround_time < thread.burst:
            errors.append(
                f"Thread {thread.thread_id}: turnaround ({thread.turnaround_time}) < burst ({thread.burst})"
            )

    # Check 4: Waiting time is non-negative
    for thread in threads:
        if thread.waiting_time < 0:
            errors.append(
                f"Thread {thread.thread_id}: negative waiting time ({thread.waiting_time})"
            )

    # Check 5: Turnaround = Waiting + Burst
    for thread in threads:
        expected = thread.waiting_time + thread.burst
        if thread.turnaround_time != expected:
            errors.append(
                f"Thread {thread.thread_id}: turnaround ({thread.turnaround_time}) != waiting ({thread.waiting_time}) + burst ({thread.burst})"
            )

    # Check 6: Completion time makes sense
    for thread in threads:
        expected_completion = thread.arrival + thread.turnaround_time
        if thread.completion_time != expected_completion:
            errors.append(f"Thread {thread.thread_id}: completion time mismatch")

    if errors:
        print(f"\n❌ VALIDATION FAILED for {algorithm_name}:")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print(f"\n✅ VALIDATION PASSED for {algorithm_name}")
        return True


def run_algorithm(algorithm_name, algorithm, threads):
    """Run a single algorithm and display results"""
    print("\n" + "=" * 70)
    print(f"ALGORITHM: {algorithm_name}")
    print("=" * 70)

    # Reset all threads
    for thread in threads:
        thread.reset()

    # Display input threads
    print("\nInput Threads:")
    print(f"{'Thread':<10}{'Arrival':<10}{'Burst':<10}{'Priority':<10}")
    print("-" * 40)
    for t in sorted(threads, key=lambda x: x.arrival):
        print(f"{t.thread_id:<10}{t.arrival:<10}{t.burst:<10}{t.priority:<10}")

    # Run simulation
    dispatcher = Dispatcher(threads, algorithm)

    tick_count = 0
    max_ticks = 1000  # Safety limit
    while not dispatcher.is_finished() and tick_count < max_ticks:
        dispatcher.tick()
        tick_count += 1

    if tick_count >= max_ticks:
        print("\n⚠️  WARNING: Simulation reached maximum tick limit!")
        return False

    # Calculate metrics
    metrics = calculate_metrics(dispatcher.threads, dispatcher.gantt_chart)

    # Display results
    print(f"\nTotal Simulation Time: {dispatcher.time_step} ticks")
    print("\nThread Results:")
    print(
        f"{'Thread':<10}{'Arrive':<10}{'Burst':<10}{'Finish':<10}{'Waiting':<10}{'Turnaround':<10}"
    )
    print("-" * 60)
    for t in sorted(threads, key=lambda x: x.thread_id):
        print(
            f"{t.thread_id:<10}{t.arrival:<10}{t.burst:<10}{t.completion_time:<10}{t.waiting_time:<10}{t.turnaround_time:<10}"
        )

    print(f"\nPerformance Metrics:")
    print(f"  Average Waiting Time    : {metrics['average_waiting_time']:.2f}")
    print(f"  Average Turnaround Time : {metrics['average_turnaround_time']:.2f}")
    print(f"  CPU Utilization         : {metrics['cpu_utilization']:.2f}%")
    print(f"  Throughput              : {metrics['throughput']:.4f} threads/tick")

    # Show Gantt chart summary (first 20 and last 20 ticks)
    print(f"\nGantt Chart Summary (first/last segments):")
    gantt_summary = []
    prev_thread = None
    start_time = 0

    for thread_id, time in dispatcher.gantt_chart:
        if thread_id != prev_thread:
            if prev_thread is not None:
                gantt_summary.append((prev_thread, start_time, time))
            prev_thread = thread_id
            start_time = time

    if prev_thread is not None:
        gantt_summary.append((prev_thread, start_time, dispatcher.time_step))

    # Show first 5 and last 5 segments
    display_count = min(5, len(gantt_summary))
    for i in range(display_count):
        thread, start, end = gantt_summary[i]
        print(f"  [{start:3d}-{end:3d}] {thread}")

    if len(gantt_summary) > 10:
        print("  ...")
        for i in range(len(gantt_summary) - display_count, len(gantt_summary)):
            thread, start, end = gantt_summary[i]
            print(f"  [{start:3d}-{end:3d}] {thread}")
    elif len(gantt_summary) > display_count:
        for i in range(display_count, len(gantt_summary)):
            thread, start, end = gantt_summary[i]
            print(f"  [{start:3d}-{end:3d}] {thread}")

    # Validate results
    is_valid = validate_results(threads, dispatcher.gantt_chart, algorithm_name)

    return is_valid


def main():
    # Set seed for reproducibility
    random.seed(42)

    print("\n" + "=" * 70)
    print("THREAD SCHEDULING SIMULATOR - COMPREHENSIVE TEST")
    print("Testing all algorithms with randomly generated threads")
    print("=" * 70)

    # Generate random threads
    num_threads = 10
    max_arrival = 15
    max_burst = 10
    max_priority = 3

    threads = generate_threads(
        num_threads=num_threads,
        max_arrival_time=max_arrival,
        burst_time_range=(1, max_burst),
        priority_range=(1, max_priority),
    )

    print(f"\nGenerated {num_threads} random threads")
    print(f"Max arrival time: {max_arrival}")
    print(f"Burst time range: 1-{max_burst}")
    print(f"Priority range: 1-{max_priority}")

    # Test all algorithms
    algorithms = [
        ("1. FCFS (First Come First Served)", FCFS()),
        ("2. SJF (Shortest Job First)", SJF()),
        ("3. Priority Scheduling", Priority()),
        ("4. Round Robin (Quantum=2)", RR(2)),
        ("5. Preemptive SJF", PreemptiveSJF()),
        ("6. Multilevel Queue (Quantum=2)", MultilevelQueue(2)),
    ]

    results = []
    for name, algorithm in algorithms:
        # Create a copy of threads for each algorithm
        thread_copies = [
            Thread(t.thread_id, t.arrival, t.burst, t.priority) for t in threads
        ]

        is_valid = run_algorithm(name, algorithm, thread_copies)
        results.append((name, is_valid))

        # Automatically continue to next algorithm
        print("\n" + "=" * 70)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY OF VALIDATION RESULTS")
    print("=" * 70)

    all_passed = True
    for name, is_valid in results:
        status = "✅ PASSED" if is_valid else "❌ FAILED"
        print(f"{status} - {name}")
        if not is_valid:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 ALL ALGORITHMS VALIDATED SUCCESSFULLY!")
    else:
        print("⚠️  SOME ALGORITHMS FAILED VALIDATION")
    print("=" * 70)


if __name__ == "__main__":
    main()
