"""
Validation script to test all algorithms with random threads
Checks correctness of outputs
"""

from algorithms.first_come_first_serve import FCFS
from algorithms.shortest_job_first import SJF
from algorithms.priority import Priority
from algorithms.round_robin import RR
from algorithms.preemptive_shortest_job_first import PreemptiveSJF
from algorithms.multilevel_queue import MultilevelQueue
from dispatcher import Dispatcher
from thread_generator import generate_threads
from metrics import calculate_metrics

def validate_output(algorithm_name, threads, dispatcher):
    """Validate the correctness of algorithm output"""
    print(f"\n{'='*70}")
    print(f"Validating: {algorithm_name}")
    print(f"{'='*70}")
    
    errors = []
    warnings = []
    
    # Check 1: All threads completed
    for thread in threads:
        if not thread.is_finished():
            errors.append(f"❌ Thread {thread.thread_id} did not complete!")
    
    # Check 2: All threads have valid completion times
    for thread in threads:
        if thread.completion_time < thread.arrival:
            errors.append(f"❌ Thread {thread.thread_id} completed before arrival!")
        if thread.completion_time < 0:
            errors.append(f"❌ Thread {thread.thread_id} has invalid completion time!")
    
    # Check 3: Turnaround time >= Burst time
    for thread in threads:
        if thread.turnaround_time < thread.burst:
            errors.append(f"❌ Thread {thread.thread_id} turnaround ({thread.turnaround_time}) < burst ({thread.burst})!")
    
    # Check 4: Waiting time = Turnaround - Burst
    for thread in threads:
        expected_waiting = thread.turnaround_time - thread.burst
        if thread.waiting_time != expected_waiting:
            errors.append(f"❌ Thread {thread.thread_id} waiting time incorrect: {thread.waiting_time} != {expected_waiting}")
    
    # Check 5: No negative values
    for thread in threads:
        if thread.waiting_time < 0:
            errors.append(f"❌ Thread {thread.thread_id} has negative waiting time!")
        if thread.turnaround_time < 0:
            errors.append(f"❌ Thread {thread.thread_id} has negative turnaround time!")
    
    # Check 6: Total CPU time should equal sum of bursts (no idle if all arrive early)
    total_burst = sum(t.burst for t in threads)
    gantt_busy_time = sum(1 for tid, _ in dispatcher.gantt_chart if tid != "IDLE")
    if gantt_busy_time != total_burst:
        warnings.append(f"⚠️  CPU busy time ({gantt_busy_time}) != total burst ({total_burst})")
    
    # Check 7: Gantt chart covers all time
    if len(dispatcher.gantt_chart) != dispatcher.time_step:
        errors.append(f"❌ Gantt chart length ({len(dispatcher.gantt_chart)}) != time steps ({dispatcher.time_step})")
    
    # Print results
    print(f"\nThread Details:")
    print(f"{'ID':<6} {'Arrive':<8} {'Burst':<8} {'Finish':<8} {'Wait':<8} {'Turnaround':<12}")
    print("-" * 60)
    for t in sorted(threads, key=lambda x: x.thread_id):
        print(f"{t.thread_id:<6} {t.arrival:<8} {t.burst:<8} {t.completion_time:<8} {t.waiting_time:<8} {t.turnaround_time:<12}")
    
    # Calculate and display metrics
    metrics = calculate_metrics(threads, dispatcher.gantt_chart)
    print(f"\nMetrics:")
    print(f"  Average Waiting Time    : {metrics['average_waiting_time']:.2f}")
    print(f"  Average Turnaround Time : {metrics['average_turnaround_time']:.2f}")
    print(f"  CPU Utilization         : {metrics['cpu_utilization']:.2f}%")
    print(f"  Throughput              : {metrics['throughput']:.4f} threads/tick")
    print(f"  Total Time              : {metrics['total_time']}")
    
    # Display validation results
    print(f"\nValidation Results:")
    if not errors and not warnings:
        print("✅ ALL CHECKS PASSED - Output is correct!")
    else:
        if errors:
            print(f"\n❌ ERRORS FOUND ({len(errors)}):")
            for error in errors:
                print(f"  {error}")
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for warning in warnings:
                print(f"  {warning}")
    
    return len(errors) == 0

def run_algorithm_test(algorithm_name, algorithm, threads):
    """Run a single algorithm and validate"""
    # Reset all threads
    for thread in threads:
        thread.reset()
    
    # Create dispatcher and run
    dispatcher = Dispatcher(threads, algorithm)
    
    # Run simulation silently
    while not dispatcher.is_finished():
        dispatcher.tick()
    
    # Validate results
    is_valid = validate_output(algorithm_name, threads, dispatcher)
    
    return is_valid

def main():
    """Main test function"""
    print("="*70)
    print("ALGORITHM VALIDATION TEST")
    print("Testing all 6 algorithms with 10 random threads")
    print("="*70)
    
    # Generate 10 random threads
    print("\nGenerating 10 random threads...")
    threads = generate_threads(
        num_threads=10,
        max_arrival_time=15,
        burst_range=(1, 10),
        priority_range=(1, 3)
    )
    
    print(f"\nGenerated Threads:")
    print(f"{'ID':<6} {'Arrive':<8} {'Burst':<8} {'Priority':<10}")
    print("-" * 40)
    for t in sorted(threads, key=lambda x: x.arrival):
        print(f"{t.thread_id:<6} {t.arrival:<8} {t.burst:<8} {t.priority:<10}")
    
    # Test all algorithms
    algorithms = [
        ("FCFS", FCFS()),
        ("SJF", SJF()),
        ("Priority", Priority()),
        ("Round Robin (Q=2)", RR(2)),
        ("Preemptive SJF", PreemptiveSJF()),
        ("Multilevel Queue (Q=2)", MultilevelQueue(2))
    ]
    
    results = {}
    for name, algorithm in algorithms:
        is_valid = run_algorithm_test(name, algorithm, threads)
        results[name] = is_valid
    
    # Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    for name, is_valid in results.items():
        status = "✅ PASSED" if is_valid else "❌ FAILED"
        print(f"{name:<30} {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 ALL ALGORITHMS PASSED VALIDATION!")
    else:
        print("\n⚠️  Some algorithms have issues - review errors above")
    
    return all_passed

if __name__ == "__main__":
    main()
