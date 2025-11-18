class Thread:
    '''
    Thread Control Block (TCB) used in thread scheduling simulations
    '''
    def __init__(self, thread_id: str, arrival_time: int, burst_time: int, priotity: int):
        # Static attributes from input
        self.thread_id: str = thread_id
        self.arrival: int = arrival_time     # when the thread arrives
        self.burst: int = burst_time         # how long it needs the CPU
        self.priority: int = priotity        # for priority scheduling

        # Simulation state
        self.remaining: int = burst_time     # decrementing as thread runs
        self.start_time: int = 0          # first time the thread gets CPU
        self.completion_time: int = 0     # time when thread finishes execution

        # Metrics
        self.waiting_time: int = 0
        self.turnaround_time: int = 0

        # internal booking-keeping fields
        self.last_run_time: int = 0 # useful on RR and SJF

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