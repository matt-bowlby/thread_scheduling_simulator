from .thread import Thread


def load_threads_from_file(filename: str):
    """Loads threads from a specified file."""
    threads = []

    # Opens the file and reads line by line
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Skip empty lines and comments

            # Split line into parts [thread_id, arrival_time, burst_time, priority]
            parts = line.split()

            # Basic validation
            if len(parts) != 4:
                print(
                    f"Error: Each line must contain exactly 4 values. Skipping line: '{line}'"
                )
                continue
            if (
                not parts[1].isdigit()
                or not parts[2].isdigit()
                or not parts[3].isdigit()
            ):
                print(
                    f"Error: Arrival time, burst time, and priority must be integers in line: '{line}'"
                )
                continue

            # Separating parts and values
            thread_id = parts[0]
            arrival_time = int(parts[1])
            burst_time = int(parts[2])
            priority = int(parts[3])

            # Create Thread object and add to list
            threads.append(Thread(thread_id, arrival_time, burst_time, priority))

    return threads
