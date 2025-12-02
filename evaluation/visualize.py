import plotly.figure_factory as ff
import pandas as pd
import random


def random_color():
    """
    Generate a random hex color code.
    """
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def display_gantt_chart(gantt_data: list[tuple[str, int]]):
    """
    Prints a formatted Gantt chart from the recorded threads (id, time) pairs.
    """

    # Handle empty gantt_data
    if not gantt_data:
        print("No Gantt data to display.")
        return

    # Merge consecutive entries of the same thread
    merged = []
    current_thread, start_time = gantt_data[0]
    for i in range(1, len(gantt_data)):
        thread, time = gantt_data[i]
        if thread != current_thread:
            # close previous block at this time
            merged.append(dict(Task=current_thread, Start=start_time, Finish=time))
            current_thread = thread
            start_time = time

    # Add the final block
    last_time = gantt_data[-1][1] + 1
    merged.append(dict(Task=current_thread, Start=start_time, Finish=last_time))

    # Convert to DataFrame
    df = pd.DataFrame(merged)
    try:
        df["Start"] = pd.to_numeric(df["Start"])
        df["Finish"] = pd.to_numeric(df["Finish"])
    except ValueError as e:
        print(f"Error converting columns to numeric: {e}")
        return  # Stop execution if data conversion fails

    # Generate colors for each thread
    unique_tasks = df["Task"].unique()
    thread_colors = {task: random_color() for task in unique_tasks}

    # Display Gantt chart
    fig = ff.create_gantt(
        df,
        index_col="Task",
        bar_width=0.4,
        show_colorbar=True,
        colors=thread_colors,
        group_tasks=True,
    )
    fig.update_layout(xaxis_type="linear")
    fig.show()


def print_metrics_table(metrics: dict, threads: list):
    """
    Print a formatted table of metrics per-thread and averages.
    Metrics come from metrics.py.
    """

    print("\n------------------- METRICS SUMMARY -------------------")
    print(
        f"{'Thread':<10}{'Arrive':<10}{'Burst':<10}{'Finish':<10}{'Waiting':<10}{'Turnaround':<12}"
    )

    for th in threads:
        print(
            f"{th.thread_id:<10}{th.arrival:<10}{th.burst:<10}{th.completion_time:<10}{th.waiting_time:<10}{th.turnaround_time:<12}"
        )

    print("\nMetrics:")
    print(f"Average Waiting Time    : {metrics['average_waiting_time']: .2f}")
    print(f"Average Turnaround Time : {metrics['average_turnaround_time']: .2f}")
    print(f"CPU Utilization         : {metrics['cpu_utilization']: .2f}%")
    print(f"Throughput              : {metrics['throughput']: .4f} threads/tick")
    print("-------------------------------------------------------\n")
