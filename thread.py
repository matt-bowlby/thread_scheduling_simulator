class Thread:
    '''
    Thread Control Block (TCB) used in thread scheduling simulations
    '''
    def __init__(self, thread_id: str, arrival_time: int, burst_time: int, priotity: int):
        # Static attributes from input
        self.thread_id: str = thread_id
        self.arrival: int = arrival_time     # when the thread arrives in steps
        self.burst: int = burst_time         # how long it needs the CPU in steps
        self.priority: int = priotity        # for priority scheduling

        # Simulation state
        self.remaining: int = burst_time     # decrementing as thread runs
        self.start_time: int = -1          # first time the thread gets CPU
        self.completion_time: int = -1     # time when thread finishes execution

        # Metrics
        self.waiting_time: int = -1
        self.turnaround_time: int = -1

        # internal booking-keeping fields
        self.last_run_time: int = -1 # useful on RR and SJF

    def is_finished(self):
        '''
            Rerturns True if the thread has finished execution (no more burst time remaining)
        '''
        return self.remaining <= 0

    def compute_metrics(self):
        '''
            Computes turnaround time and waiting time for the thread after completion
        '''
        self.turnaround_time = self.completion_time - self.arrival
        self.waiting_time = self.turnaround_time - self.burst

    def reset(self) -> None:
        '''
            Resets the thread to its initial state for re-simulation
        '''
        self.remaining = self.burst
        self.start_time = -1
        self.completion_time = -1
        self.waiting_time = -1
        self.turnaround_time = -1
        self.last_run_time = -1

    def run(self, current_time_step: int) -> None:
        self.remaining -= 1
        self.last_run_time = current_time_step
        if self.start_time == -1:
            self.start_time = current_time_step
        if self.is_finished():
            self.completion_time = current_time_step + 1
            self.compute_metrics()