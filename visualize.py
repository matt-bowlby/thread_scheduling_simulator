def print_gantt_chart (gantt_data: list[tuple[str,int]]):
    '''
    Prints a formatted Gantt chart from the recorded threads (id, time) pair
    Highlights preemptions and idle CPU periods'''

    if not gantt_data:
        print("No Gantt data to display.")
        return
    
    print("\n----------- GANTT CHART ----------")

    merged = []
    current_thread, start_time = gantt_data[0]

    # fiish here

def print_metrics_table (metrics: dict, threads: list):
    '''
    Print a formatted table of metrics per thread and averages
    Metrics come from mentrics.py'''

    print("\n----------- METRICS SUMMARY ----------")

    # finish here 
    return 
