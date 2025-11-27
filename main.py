import time

from algorithms.first_come_first_serve import FCFS
from algorithms.shortest_job_first import SJF
from algorithms.priority import Priority
from algorithms.round_robin import RR
from algorithms.preemptive_shortest_job_first import PreemptiveSJF
from algorithms.multilevel_queue import MultilevelQueue

from dispatcher import Dispatcher
from thread_file_loader import load_threads_from_file
from thread_generator import generate_threads

from metrics import calculate_metrics
from visualize import display_gantt_chart, print_metrics_table
from thread import Thread
from algorithms import Algorithm

TICK_RATE = 100 # Ticks per second

def run(threads: list[Thread], algorithm: Algorithm) -> None:
	tick_interval = 1.0 / TICK_RATE
	next_tick = time.time() + tick_interval

	dispatcher = Dispatcher(threads, algorithm)

	# Main loop
	while not dispatcher.is_finished():
		dispatcher.tick()

		# Wait until the next tick
		sleep_duration = next_tick - time.time()
		if sleep_duration > 0:
			time.sleep(sleep_duration)
		next_tick += tick_interval

	# Simulation Finished
	total_time = dispatcher.time_step
	print("\n---------- SIMULATION COMPLETE ----------")
	print(f"Total Time: {total_time} ticks\n")

	# Print Metrics and Gantt Chart
	metrics = calculate_metrics(dispatcher.threads, dispatcher.gantt_chart)
	display_gantt_chart(dispatcher.gantt_chart)
	print_metrics_table(metrics, dispatcher.threads)


def main():
	print("Welcome to the thread scheduling simulator.")
	while True:
		print("Please select an algorithm to run:")
		print("1. FCFS")
		print("2. SJF")
		print("3. Priority")
		print("4. Round Robin")
		print("5. Preemptive SJF")
		print("6. Multilevel Queue")
		print("0. Exit")
		choice = input("Please enter your choice: ")

		algorithm = None
		match choice:
			case "0":
				break
			case "1":
				algorithm = FCFS()
			case "2":
				algorithm = SJF()
			case "3":
				algorithm = Priority()
			case "4":
				quantum = int(input("Please specify a qauntum: "))
				algorithm = RR(quantum)
			case "5":
				algorithm = PreemptiveSJF()
			case "6":
				quantum = int(input("Please specify a qauntum: "))
				algorithm = MultilevelQueue(quantum)
			case _:
				print("Invalid choice. Please try again.")
				continue

		print("How do you want to input threads?")
		print("1. From a file")
		print("2. From the console")
		print("3. Randomly generate")
		choice = input("Please enter your choice: ")

		threads = []
		match choice:
			case "1":
				while True:
					file_name = input("Please specify a file name: ")
					try:
						threads = load_threads_from_file(file_name)
					except FileNotFoundError:
						print("File not found. Please try again.")
					else:
						break
			case "2":
				threads = []
				while True:
					try:
						thread_id = input("Please specify a thread ID: ")
						arrival = int(input("Please specify an arrival time: "))
						burst = int(input("Please specify a burst time: "))
						priority = int(input("Please specify a priority: "))
						threads.append(Thread(thread_id, arrival, burst, priority))
						if input("Do you want to add another thread? (y/n): ") == "n":
							break
					except ValueError:
						print("Invalid input. Please try again.")
			case "3":
				while True:
					num = 0
					max_arrival_time = 0
					max_burst_time = 0
					max_priority = 0
					try:
						num = int(input("Enter the number of threads: "))
						max_arrival_time = int(input("Enter the maximum arrival time: "))
						max_burst_time = int(input("Enter the maximum burst time: "))
						max_priority = int(input("Enter the maximum priority: "))
					except ValueError:
						print("Invalid input. Please try again.")
					else:
						threads = generate_threads(num, max_arrival_time, (1, max_burst_time), (1, max_priority))
						break
			case _:
				print("Invalid choice. Please try again.")

		print("Running threads...\n")
		run(threads, algorithm)
		input("Press enter to continue...")



if __name__ == "__main__":
	main()