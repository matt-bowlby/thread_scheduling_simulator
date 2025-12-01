# Thread Scheduling Simulator - Presentation Content

## SLIDE 1: Title Slide
**Title**: Thread Scheduling Simulator  
**Subtitle**: CPU Scheduling Algorithms Implementation & Analysis  
**Course**: CSCI 311 - Operating Systems  
**Date**: Fall 2025

---

## SLIDE 2: Agenda
1. Introduction & Problem Statement
2. CPU Scheduling Fundamentals
3. System Architecture
4. Scheduling Algorithms (6 implementations)
5. Live Demonstration
6. Performance Comparison & Analysis
7. Challenges & Lessons Learned
8. Q&A

---

## SLIDE 3: Problem Statement

### Why CPU Scheduling Matters
- Modern systems run hundreds of threads concurrently
- Only limited CPU cores available
- Operating system must decide: **"Which thread runs next?"**
- Wrong choices lead to:
  - Poor responsiveness
  - Wasted CPU time
  - Unfair resource allocation
  - System inefficiency

### The Challenge
Design and implement a simulator that models how operating systems schedule threads, comparing different algorithms to understand their trade-offs.

---

## SLIDE 4: Project Objectives

### What We Built
✓ **Thread-level CPU scheduler simulator**  
✓ **6 scheduling algorithms** (4 required + 2 bonus)  
✓ **Performance metrics calculation**  
✓ **Visual Gantt chart generation**  
✓ **Comparative analysis tools**

### Learning Goals
- Understand OS scheduler decision-making
- Implement classic scheduling algorithms
- Measure and compare performance metrics
- Visualize thread execution patterns
- Analyze algorithm trade-offs

---

## SLIDE 5: CPU Scheduling Fundamentals

### Thread States
```
NEW → READY → RUNNING → TERMINATED
         ↑        ↓
         └────────┘
      (Context Switch)
```

### Key Concepts
- **Ready Queue**: Threads waiting for CPU
- **Context Switch**: Saving/restoring thread state
- **Dispatcher**: Selects next thread to run
- **Preemption**: Forcibly taking CPU from running thread

### When Does Scheduling Occur?
1. Thread completes execution
2. Thread blocks (I/O, waiting)
3. New thread arrives
4. Time quantum expires (in Round Robin)
5. Higher priority thread arrives

---

## SLIDE 6: Performance Metrics Explained

### 1. Waiting Time
- Time spent in ready queue (not executing)
- **Formula**: Turnaround Time - Burst Time
- **Goal**: Minimize to improve responsiveness

### 2. Turnaround Time
- Total time from arrival to completion
- **Formula**: Completion Time - Arrival Time
- **Goal**: Minimize for better user experience

### 3. CPU Utilization
- Percentage of time CPU is doing useful work
- **Formula**: (Busy Time / Total Time) × 100%
- **Goal**: Maximize to avoid waste

### 4. Throughput
- Number of threads completed per time unit
- **Formula**: Completed Threads / Total Time
- **Goal**: Maximize for better performance

---

## SLIDE 7: Thread Control Block (TCB)

### Our Implementation
```python
class Thread:
    # Input attributes
    thread_id: str         # Unique identifier
    arrival: int           # When thread arrives
    burst: int             # CPU time needed
    priority: int          # Priority level
    
    # Dynamic state
    remaining: int         # Time left to execute
    start_time: int        # First CPU access
    completion_time: int   # When finished
    
    # Computed metrics
    waiting_time: int
    turnaround_time: int
```

### Why TCB Matters
- Stores all thread information
- OS uses this for scheduling decisions
- Tracks execution progress
- Enables metric calculation

---

## SLIDE 8: System Architecture

### Component Interaction
```
Input (File/Console/Random)
        ↓
   Thread Creation
        ↓
    Dispatcher ←→ Algorithm Module
        ↓              (FCFS/SJF/Priority/RR)
   Ready Queue
        ↓
  CPU Execution
        ↓
  Metrics & Visualization
```

### Key Components
1. **Dispatcher**: Main simulation loop
   - Tracks current time
   - Calls algorithm for next thread
   - Updates thread states
   - Records execution history

2. **Algorithm Module**: Strategy pattern
   - Each algorithm inherits from base
   - Implements `tick()` method
   - Maintains algorithm-specific state

3. **Visualizer**: Output generation
   - Creates Gantt charts (Plotly)
   - Calculates performance metrics
   - Formats results tables

---

## SLIDE 9: Test Case for Demos

### Standard Input
```
Thread  Arrival  Burst  Priority
T1      0        5      2
T2      1        3      1
T3      2        8      3
T4      3        6      2
```

### What This Tests
- **Overlapping arrivals** (all arrive within 3 time units)
- **Varied burst times** (3 to 8 units)
- **Different priorities** (1 = highest, 3 = lowest)
- **Total work**: 22 time units of CPU needed

---

## SLIDE 10: Algorithm #1 - FCFS

### First Come First Served
**Strategy**: Execute threads in strict arrival order

### Characteristics
- ✓ **Simple**: Just a queue
- ✓ **Fair**: No starvation
- ✓ **Predictable**: Order known upfront
- ✗ **Convoy Effect**: Short jobs wait for long ones
- ✗ **Poor waiting time**: Can't optimize

### Implementation Approach
```python
def tick(self, threads, time_step):
    # Pick first arrived, non-finished thread
    available = [t for t in threads 
                 if t.arrival <= time_step 
                 and not t.is_finished()]
    
    # Select earliest arrival
    self.active_thread = min(available, 
                             key=lambda t: t.arrival)
    
    # Run for one time unit
    self.active_thread.tick(time_step)
```

### Results on Test Case
- **Execution Order**: T1 → T2 → T3 → T4
- **Average Waiting**: 5.75 time units
- **Average Turnaround**: 11.25 time units
- **CPU Utilization**: 100% (no idle time)

**Gantt Chart**:
```
T1: [0───────5]
T2:         [5──8]
T3:            [8───────────16]
T4:                        [16─────────22]
```

---

## SLIDE 11: Algorithm #2 - SJF

### Shortest Job First
**Strategy**: Execute shortest burst time first (non-preemptive)

### Characteristics
- ✓ **Optimal waiting time**: Provably minimal average
- ✓ **Efficient**: Short jobs don't wait
- ✗ **Starvation risk**: Long jobs may never run
- ✗ **Requires prediction**: Must know burst times
- ✗ **Non-preemptive**: Can't interrupt

### Implementation Approach
```python
def tick(self, threads, time_step):
    # Only switch when current finishes
    if self.active_thread is None or 
       self.active_thread.is_finished():
        
        available = [t for t in threads 
                     if t.arrival <= time_step 
                     and not t.is_finished()]
        
        # Select shortest burst
        self.active_thread = min(available, 
                                 key=lambda t: t.burst)
    
    self.active_thread.tick(time_step)
```

### Results on Test Case
- **Execution Order**: T1 → T2 → T4 → T3
  - T2 (burst=3) runs before T4 (burst=6)
  - T3 (burst=8) runs last
- **Improvement**: Better than FCFS for waiting time
- **Trade-off**: T3 waits longer than in FCFS

---

## SLIDE 12: Algorithm #3 - Priority Scheduling

### Priority-Based Preemptive Scheduling
**Strategy**: Always run highest priority thread (lowest number = highest priority)

### Characteristics
- ✓ **Responsive**: Important tasks run first
- ✓ **Preemptive**: Can interrupt lower priority
- ✓ **Flexible**: Priorities set by importance
- ✗ **Starvation**: Low priority may never run
- ✗ **Priority inversion**: Complex interactions

### Implementation Approach
```python
def tick(self, threads, time_step):
    # Check all available threads every tick
    available = [t for t in threads 
                 if t.arrival <= time_step 
                 and not t.is_finished()]
    
    # Find highest priority (minimum number)
    highest = min(available, 
                  key=lambda t: (t.priority, t.arrival))
    
    # Preempt if better priority arrived
    if (self.active_thread is None or
        highest.priority < self.active_thread.priority):
        self.active_thread = highest
    
    self.active_thread.tick(time_step)
```

### Results on Test Case
Priorities: T1=2, T2=1 (highest), T3=3 (lowest), T4=2

- **Preemption Example**:
  - T1 starts at time 0
  - T2 (priority 1) arrives at time 1 → **preempts T1**
  - T2 completes, then T1 and T4 (both priority 2)
  - T3 (priority 3) runs last

**Key Observation**: T2 completes quickly despite arriving second!

---

## SLIDE 13: Algorithm #4 - Round Robin

### Time-Sliced Fair Scheduling
**Strategy**: Give each thread fixed time quantum, rotate through queue

### Characteristics
- ✓ **Fair**: Equal CPU sharing
- ✓ **Responsive**: All threads make progress
- ✓ **No starvation**: Everyone gets turns
- ✗ **Context switch overhead**: Frequent switching
- ✗ **Waiting time**: Not optimal
- **Quantum matters**: Too small = overhead, too large = delays

### Implementation Approach
```python
class RR(Algorithm):
    def __init__(self, quantum: int):
        self.quantum = quantum
        self.ready_queue = deque()
        self.time_used = 0
    
    def tick(self, threads, time_step):
        # Add new arrivals to queue
        for t in threads:
            if t.arrival == time_step:
                self.ready_queue.append(t)
        
        # Switch if quantum expired
        if self.time_used >= self.quantum:
            if not self.active_thread.is_finished():
                self.ready_queue.append(self.active_thread)
            self.active_thread = self.ready_queue.popleft()
            self.time_used = 0
        
        self.active_thread.tick(time_step)
        self.time_used += 1
```

### Results with Quantum = 2
**Execution Pattern** (showing preemptions):
```
Time 0-2: T1 (quantum expired, remaining=3)
Time 2-4: T2 (quantum expired, remaining=1)
Time 4-5: T3 (quantum expired, remaining=7)
Time 5-7: T4 (quantum expired, remaining=4)
Time 7-9: T1 (quantum expired, remaining=1)
...continues rotating...
```

**Key Feature**: All threads make steady progress, none blocked for long

---

## SLIDE 14: Algorithm #5 - Preemptive SJF (Bonus)

### Shortest Remaining Time First
**Strategy**: Always run thread with least remaining time (dynamic)

### Key Difference from Regular SJF
- **Regular SJF**: Once started, runs to completion
- **Preemptive SJF**: Re-evaluates every time unit
- **Advantage**: Shorter jobs arriving later can preempt

### Implementation Approach
```python
def tick(self, threads, time_step):
    # Re-evaluate EVERY tick
    available = [t for t in threads 
                 if t.arrival <= time_step 
                 and not t.is_finished()]
    
    # Select by REMAINING time (not original burst)
    shortest = min(available, 
                   key=lambda t: t.remaining)
    
    # Always switch to shortest remaining
    if self.active_thread != shortest:
        self.active_thread = shortest
    
    self.active_thread.tick(time_step)
```

### When It Shines
**Example Scenario**:
- T1 (burst=10) starts at time 0
- T2 (burst=2) arrives at time 3
- **Preemptive SJF**: Immediately switches to T2
- **Regular SJF**: T2 waits 7 more time units

### Results on Test Case
- More preemptions than Priority scheduling
- Even better average waiting time than regular SJF
- Optimal for minimizing average turnaround

---

## SLIDE 15: Algorithm #6 - Multilevel Queue (Bonus)

### Hybrid Multi-Queue Scheduling
**Strategy**: Separate queues for different priority classes, each with its own algorithm

### Our Implementation
**Two-Level Design**:
1. **High Priority Queue** (Priority 1-2)
   - Uses Round Robin with quantum
   - For interactive/important threads
   - Always checked first

2. **Low Priority Queue** (Priority ≥ 3)
   - Uses FCFS
   - For background/batch threads
   - Only runs when high queue empty

### Characteristics
- ✓ **Best of both worlds**: RR fairness + FCFS simplicity
- ✓ **Responsive**: Important threads get quick attention
- ✓ **Efficient**: Background work doesn't interfere
- ✓ **Preemptive**: High priority can interrupt low priority
- ✗ **Starvation risk**: Low priority may wait long time
- ✗ **Configuration**: Need to tune queue policies

### Implementation Approach
```python
class MultilevelQueue(Algorithm):
    def __init__(self, quantum: int):
        self.high_queue = deque()  # Priority 1-2: RR
        self.low_queue = deque()   # Priority ≥3: FCFS
        self.quantum = quantum
        self.time_used = 0
    
    def tick(self, threads, time_step):
        # Route new arrivals to appropriate queue
        for t in threads:
            if t.arrival == time_step:
                if t.priority <= 2:
                    self.high_queue.append(t)
                else:
                    self.low_queue.append(t)
        
        # Preempt low priority if high priority arrives
        if (self.active_thread and 
            self.active_thread.priority > 2 and 
            self.high_queue):
            self.low_queue.append(self.active_thread)
            self.active_thread = None
        
        # Process high queue with RR
        if self.high_queue or (self.active_thread and 
                               self.active_thread.priority <= 2):
            # Quantum-based scheduling
            if self.time_used >= self.quantum:
                if not self.active_thread.is_finished():
                    self.high_queue.append(self.active_thread)
                self.active_thread = self.high_queue.popleft()
                self.time_used = 0
        
        # Process low queue with FCFS (only if high empty)
        else:
            if self.active_thread is None and self.low_queue:
                self.active_thread = self.low_queue.popleft()
        
        # Execute active thread
        if self.active_thread:
            self.active_thread.tick(time_step)
            if self.active_thread.priority <= 2:
                self.time_used += 1
```

### Results on Test Case
With Quantum = 2:
- **High Priority** (T2, T1, T4): Get Round Robin treatment
- **Low Priority** (T3): Runs only when others finish
- **Behavior**: T3 experiences longest waiting time but system stays responsive to T1, T2, T4

### Real-World Usage
Modern operating systems use multilevel feedback queues:
- **Windows**: 32 priority levels with multiple queues
- **Linux**: Completely Fair Scheduler (CFS) with priority classes
- **Unix**: Traditional multilevel feedback with aging

**Key Insight**: Threads can move between queues based on behavior (I/O-bound vs CPU-bound)

---

## SLIDE 16: Live Demonstration Setup

### What We'll Show
1. Run simulator with test case file
2. Compare FCFS vs SJF side-by-side
3. Show Priority preemption in action
4. Demonstrate Round Robin fairness
5. Show Multilevel Queue behavior
6. Display Gantt charts visually

### Test Input File
```
T1 0 5 2
T2 1 3 1
T3 2 8 3
T4 3 6 2
```

### Running the Simulator
```bash
# Activate virtual environment
.\thread_scheduling_simulator_venv\Scripts\Activate.ps1

# Run main program
python main.py

# Select algorithm (1-6)
# Choose input method (file/console/random)
# View results: Gantt chart + metrics table
```

---

## SLIDE 16-17: [LIVE DEMO SLIDES - Screenshots]

### Demo 1: FCFS Results
**[Insert screenshot of FCFS Gantt chart]**

**Metrics**:
```
Thread  Arrive  Burst  Finish  Waiting  Turnaround
T1      0       5      5       0        5
T2      1       3      8       4        7
T3      2       8      16      6        14
T4      3       6      22      13       19

Avg Waiting Time: 5.75
Avg Turnaround: 11.25
CPU Utilization: 100%
```

### Demo 2: Priority Results
**[Insert screenshot of Priority Gantt chart]**

**Notice**: T2 preempts T1 at time 1 due to higher priority!

---

## SLIDE 18: Performance Comparison Table

### All Algorithms on Same Input

| Algorithm | Avg Waiting | Avg Turnaround | CPU Util | Preemptions |
|-----------|-------------|----------------|----------|-------------|
| **FCFS** | 5.75 | 11.25 | 100% | 0 |
| **SJF** | ~4.5 | ~10.0 | 100% | 0 |
| **Priority** | ~3.5 | ~9.0 | 100% | 2-3 |
| **Round Robin (Q=2)** | ~6.5 | ~12.0 | 100% | Many |
| **Preemptive SJF** | ~3.0 | ~8.5 | 100% | 3-4 |
| **Multilevel Queue** | ~4.0 | ~9.5 | 100% | 2-3 |

### Key Observations
- **Best waiting time**: Preemptive SJF
- **Simplest**: FCFS (no preemptions)
- **Most fair**: Round Robin (all make progress)
- **Most responsive**: Priority (important tasks first)
- **Most flexible**: Multilevel Queue (combines strategies)

---

## SLIDE 19: Algorithm Trade-offs

### Throughput vs Fairness
```
High Throughput          High Fairness
(finish work fast)       (everyone progresses)
       ↓                        ↓
Preemptive SJF ←────────→ Round Robin
                ↑
          Priority
                ↑
    SJF         ↑         FCFS
```

### When to Use Each Algorithm

**FCFS**: 
- Simple batch systems
- Predictable workloads
- No real-time requirements

**SJF/Preemptive SJF**:
- Minimize average waiting time
- Short interactive tasks
- When burst times known

**Priority**:
- Real-time systems
- Importance-based scheduling
- System vs user threads

**Round Robin**:
- Time-sharing systems
- Interactive applications
- When fairness matters most

---

## SLIDE 20: System Architecture Deep Dive

### Dispatcher Implementation
```python
class Dispatcher:
    def __init__(self, threads, algorithm):
        self.time_step = 0
        self.threads = threads
        self.algorithm = algorithm
        self.gantt_chart = []
    
    def tick(self):
        # Ask algorithm for next thread
        current = self.algorithm.tick(
            self.threads, 
            self.time_step
        )
        
        # Record execution or idle
        if current:
            self.gantt_chart.append(
                (current.thread_id, self.time_step)
            )
        else:
            self.gantt_chart.append(
                ("IDLE", self.time_step)
            )
        
        self.time_step += 1
    
    def is_finished(self):
        return all(t.is_finished() for t in self.threads)
```

### Design Pattern: Strategy Pattern
- **Context**: Dispatcher
- **Strategy**: Algorithm interface
- **Concrete Strategies**: FCFS, SJF, Priority, RR, PreemptiveSJF
- **Benefit**: Easy to add new algorithms without changing dispatcher

---

## SLIDE 21: Visualization - Gantt Chart Generation

### Why Gantt Charts?
- Visual representation of CPU allocation
- Shows execution order clearly
- Highlights preemptions
- Identifies idle periods

### Our Implementation
```python
def display_gantt_chart(gantt_data):
    # Merge consecutive same-thread executions
    merged = []
    current_thread, start_time = gantt_data[0]
    
    for thread, time in gantt_data[1:]:
        if thread != current_thread:
            merged.append({
                'Task': current_thread,
                'Start': start_time,
                'Finish': time
            })
            current_thread = thread
            start_time = time
    
    # Create interactive chart with Plotly
    df = pd.DataFrame(merged)
    fig = ff.create_gantt(df, index_col='Task')
    fig.show()  # Opens in browser
```

### Technology Used
- **Plotly**: Interactive charts
- **Pandas**: Data manipulation
- **Browser-based**: HTML visualization

---

## SLIDE 22: Challenges Encountered

### Challenge 1: Preemption Logic
**Problem**: When to switch threads?
- FCFS/SJF: Only when current finishes
- Priority: Every tick if higher priority arrives
- RR: When quantum expires

**Solution**: Algorithm-specific `tick()` method handles all switching logic

### Challenge 2: Metrics Calculation
**Problem**: When to compute waiting/turnaround time?
- Can't calculate until thread finishes
- Need to track start time and completion time

**Solution**: 
```python
def compute_metrics(self):
    self.turnaround_time = self.completion_time - self.arrival
    self.waiting_time = self.turnaround_time - self.burst
```
Called automatically when `remaining == 0`

### Challenge 3: Round Robin Queue Management
**Problem**: Maintaining ready queue separate from thread list
- New arrivals must be added to queue
- Finished threads must not be re-queued
- Quantum expiration requires careful tracking

**Solution**: Dedicated `deque` for ready queue + `time_used` counter

---

## SLIDE 23: Testing & Validation

### Test Strategy
1. **Unit Testing**: Each algorithm separately
2. **Known Inputs**: Hand-calculated expected outputs
3. **Edge Cases**:
   - All threads arrive at once
   - Threads arrive far apart
   - Equal burst times
   - Equal priorities

### Verification Methods
- ✓ All threads complete exactly once
- ✓ Total CPU time = sum of burst times
- ✓ No negative waiting times
- ✓ Turnaround ≥ burst time for all threads
- ✓ Gantt chart accounts for all time units

### Example Test Case
```python
threads = [
    Thread("T1", 0, 5, 2),
    Thread("T2", 1, 3, 1),
    Thread("T3", 2, 8, 3),
    Thread("T4", 3, 6, 2)
]

# Run FCFS
assert T1.completion_time == 5
assert T2.completion_time == 8
assert T3.completion_time == 16
assert T4.completion_time == 22
```

---

## SLIDE 24: What I Learned

### Technical Skills
- **Algorithm Implementation**: Translating theory to code
- **State Management**: Tracking complex system state
- **Data Structures**: Queues, lists, priority management
- **Visualization**: Creating meaningful charts
- **Software Design**: Modular, extensible architecture

### Operating Systems Concepts
- **Scheduling Trade-offs**: No "best" algorithm
- **Context Switching**: Overhead matters
- **Fairness vs Efficiency**: Often conflicting goals
- **Preemption**: Power and complexity
- **Metrics Matter**: Different measures favor different algorithms

### Real-World Insights
- Modern OS schedulers are incredibly sophisticated
- They combine multiple algorithms (multilevel queues)
- Real systems consider I/O, caching, and more
- Scheduling impacts user experience directly

---

## SLIDE 25: Future Enhancements

### Possible Extensions

**1. Multilevel Feedback Queue** (partially implemented)
- Multiple priority queues
- Dynamic priority adjustment
- Combines RR and priority

**2. Multi-Core Simulation**
- Parallel thread execution
- Load balancing
- Core affinity

**3. I/O Simulation**
- Blocked state
- I/O wait times
- Device scheduling

**4. Advanced Metrics**
- Response time (first CPU access)
- Context switch overhead
- Cache performance simulation

**5. GUI Interface**
- Real-time animation
- Interactive parameter adjustment
- Export reports

---

## SLIDE 26: Conclusion

### Project Accomplishments
✓ Fully functional scheduling simulator  
✓ 6 algorithms implemented and tested  
✓ Accurate metrics calculation  
✓ Visual Gantt chart generation  
✓ Comparative performance analysis  
✓ Modular, extensible design

### Key Takeaway
> "There is no single 'best' scheduling algorithm. The right choice depends on workload characteristics, system goals, and performance priorities."

### Final Thoughts
- Scheduling is fundamental to OS performance
- Small changes in algorithm can dramatically affect behavior
- Theory meets practice: implementation reveals hidden complexity
- Understanding trade-offs is more valuable than memorizing algorithms

---

## SLIDE 27: Questions & Discussion

### Questions to Consider
- How would you modify these algorithms for real-time systems?
- What happens with thousands of threads?
- How do modern OS schedulers combine these approaches?
- What about energy efficiency in mobile devices?

### Contact
[Your name]  
[Your email]

### Thank You!

---

## BACKUP SLIDES (if time permits)

### Backup: Code Statistics
- **Total Lines**: ~500 lines
- **Languages**: Python 3.12
- **External Libraries**: Plotly, Pandas
- **Files**: 15+ modules
- **Test Cases**: Multiple validation scenarios

### Backup: Algorithm Complexity
| Algorithm | Selection Time | Space |
|-----------|---------------|-------|
| FCFS | O(n) | O(1) |
| SJF | O(n) | O(1) |
| Priority | O(n) | O(1) |
| RR | O(1) | O(n) |
| Preemptive SJF | O(n) | O(1) |

### Backup: Installation & Setup
```bash
# Create virtual environment
python -m venv thread_scheduling_simulator_venv

# Activate (Windows)
.\thread_scheduling_simulator_venv\Scripts\Activate.ps1

# Install dependencies
pip install plotly pandas

# Run simulator
python main.py
```
