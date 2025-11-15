from thread import Thread
def load_thread_from_file(filename: str): 
    threads = []

    with open(filename, 'r') as file: 
        for line in file: 
            line = line.strip()
            if not line or line.startswith('#'):
                continue                        # Skip empty lines and comments

            parts = line.split()
            if len(parts) != 4: 
                raise ValueError(f"Invalid line format: '{line}'")
            
            # separating parts and values
            thread_id = parts[0]
            arrival_time = int(parts[1])
            burst_time = int(parts[2])
            priority = int(parts[3])

            threads.append(Thread(thread_id, arrival_time, burst_time, priority))

    # sorting the threads by arrival time
    threads.sort(key=lambda t: t.arrival)
    return threads      
