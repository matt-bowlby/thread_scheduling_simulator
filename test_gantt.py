"""
Quick test to verify Gantt chart visualization works
"""

from algorithms.first_come_first_serve import FCFS
from dispatcher import Dispatcher
from thread import Thread
from metrics import calculate_metrics
from visualize import display_gantt_chart, print_metrics_table

print("Testing Gantt Chart Visualization...")
print("="*60)

# Create simple test case
threads = [
    Thread("T1", 0, 3, 1),
    Thread("T2", 1, 2, 2),
    Thread("T3", 2, 4, 1)
]

print("\nRunning FCFS with 3 threads...")
dispatcher = Dispatcher(threads, FCFS())

while not dispatcher.is_finished():
    dispatcher.tick()

print(f"\nSimulation complete in {dispatcher.time_step} ticks")

# Calculate metrics
metrics = calculate_metrics(dispatcher.threads, dispatcher.gantt_chart)

# Display Gantt chart (should open in browser)
print("\nGenerating Gantt chart...")
print("(This should open an interactive chart in your browser)")
display_gantt_chart(dispatcher.gantt_chart)

# Print metrics table
print_metrics_table(metrics, dispatcher.threads)

print("\n" + "="*60)
print("✅ If a browser window opened with the Gantt chart,")
print("   the visualization is working correctly!")
print("="*60)
