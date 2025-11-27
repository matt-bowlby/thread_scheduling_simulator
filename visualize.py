import plotly.figure_factory as ff
import pandas as pd

def display_gantt_chart(gantt_data: list[tuple[str, int]]):
    '''
    Prints a formatted Gantt chart from the recorded threads (id, time) pair
    Highlights preemptions and idle CPU periods'''

    if not gantt_data:
        print("No Gantt data to display.")
        return

    merged = []
    current_thread, start_time = gantt_data[0]

    for i in range(1, len(gantt_data)):
        thread, time = gantt_data[i]

        if thread != current_thread:
            # close previous block at this time
            merged.append(dict(Task=current_thread, Start=start_time, Finish=time))
            current_thread = thread
            start_time = time

    # add the final block
    last_time = gantt_data[-1][1] + 1
    merged.append(dict(Task=current_thread, Start=start_time, Finish=last_time))

    print(merged)

    # Convert to DataFrame
    df = pd.DataFrame(merged)
    try:
        df['Start'] = pd.to_numeric(df['Start'])
        df['Finish'] = pd.to_numeric(df['Finish'])
    except ValueError as e:
        print(f"Error converting columns to numeric: {e}")
        return # Stop execution if data conversion fails

    fig = ff.create_gantt(df, index_col='Task', bar_width=0.4, show_colorbar=True)
    fig.update_layout(xaxis_type='linear')
    fig.show()


    # Execution summary per thread
    # executed_totals = {}



    # # print the merge blocks
    # for thread, start, end in merged:
    #     if thread != "IDLE" :
    #         duration = end- start
    #         executed_totals[thread] = executed_totals.get(thread,0) + duration

    # # Determining full busrts sizes
    # global_threads = {th.thread_id: th for th in getattr(display_gantt_chart, "threads", [])}

    # # running execution so far per thread
    # running_exec = {th: 0 for th in executed_totals}

    # # Print merged blocks with status
    # for thread, start, end in merged:
    #     duration = end - start

    #     if thread == "IDLE":
    #         print(f"[{start:02d} - {end:02d}] CPU IDLE ({duration} unit)")
    #         continue

    #     total_burst = global_threads[thread].burst
    #     # update running executed after thius block
    #     running_exec[thread] += duration
    #     remaining_after = total_burst - running_exec[thread]

    #     if remaining_after == 0:
    #         status = "finished"
    #     else:
    #         status = f"remaining: {remaining_after}"

    #     print(f"[{start:02d} - {end:02d}] {thread:<5} ran ({duration} units, {status})")

    # print("--------------------------------------------------\n")

def print_metrics_table (metrics: dict, threads: list):
    '''
    Print a formatted table of metrics per thread and averages
    Metrics come from mentrics.py'''

    print("\n------------------- METRICS SUMMARY -------------------")
    print(f"{'Thread':<10}{'Arrive':<10}{'Burst':<10}{'Finish':<10}{'Waitign':<10}{'Turnaround':<12}")

    for th in threads:
        print(f"{th.thread_id:<10}{th.arrival:<10}{th.burst:<10}{th.completion_time:<10}{th.waiting_time:<10}{th.turnaround_time:<12}")

    print("\nAverages:")
    print(f"Average Waiting Time    : {metrics['average_waiting_time']: .2f}")
    print(f"Average Turnaround Time : {metrics['average_turnaround_time']: .2f}")
    print(f"CPU Utilization         : {metrics['cpu_utilization']: .2f}%")
    print(f"Throughput              : {metrics['throughput']: .4f} threads/tick")
    print("-------------------------------------------------------\n")