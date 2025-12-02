# Thread Scheduling Simulator

This project is a Thread Scheduling Simulator implemented in Python. It simulates various thread scheduling algorithms to help understand their behavior and performance.

## Algorithms

- First-Come, First-Serve
	> Executes threads in the order they arrive.
- Shortest Job First
	> Executes the thread with the smallest burst time next.
- Round Robin
	> Each thread is assigned a fixed time slice in a cyclic order.
- Priority Scheduling
	> Executes threads based on their priority.
- Multilevel Queue Scheduling
	> Divides threads into multiple queues based on priority and schedules them accordingly.
- Preemptive Shortest Job First
	> Similar to SJF but allows preemption if a new thread arrives with a shorter burst time.

## Project file structure

- `algorithms/`: Contains implementations of various scheduling algorithms.
- `thread_handling/`: Contains classes and functions for managing threads.
- `evaluation/`: Contains modules for evaluating and visualizing scheduling results.
- `dispatcher.py`: Manages the scheduling process using the selected algorithm.
- `main.py`: Entry point for running the simulator. Contains the input prompting and CLI logic.

## Project System Structure

- `main.py`: The main entry point of the simulator. This file handles user input and initiates the simulation. The user will supply the algorithm, thread details, and other parameters here through the CLI. It then passes this information to the dispatcher.
- `dispatcher.py`: The dispatcher is responsible for managing the scheduling of threads using the selected algorithm. It ticks through time, assigns threads to the CPU based on the algorithm's logic, and collects scheduling data for evaluation.
- `algorithms/`: This directory contains the implementations of various scheduling algorithms, each in its own module. Each algorithm module defines how threads are selected and scheduled.
- `thread_handling/`: This directory contains the `Thread` class and any related functions for managing thread attributes and states.

## Project flow

1. Define threads with their attributes (arrival time, burst time, priority, etc.).
2. Select a scheduling algorithm.
3. The dispatcher uses the selected algorithm to schedule the threads.
4. Evaluate the scheduling results using various metrics.
5. Visualize the results using Gantt charts and metrics tables.

## Data Structures

- **Thread Class**: Represents a thread with attributes like ID, arrival time, burst time, priority, etc.
- **Algorithm Base Class**: An abstract base class for all scheduling algorithms, defining the interface for scheduling methods.
- **Dispatcher Class**: Manages the scheduling process and interacts with the selected algorithm.

## Dependencies

- Python 3.x
- plotly.express
- pandas

## Running the Simulator

1. Ensure you have Python 3.x installed.
2. Install the required dependencies using pip:
   ```bash
   pip install plotly pandas
   ```
3. Run the simulator using the command line:
   ```bash
   python main.py
   ```