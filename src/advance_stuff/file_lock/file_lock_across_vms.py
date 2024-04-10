import os
import time
import fcntl

lock_file = "/path/to/lockfile.lock"
counter_file = "/path/to/counterfile.txt"
process_name = "processA"
max_instances = 2

def acquire_lock():
    while True:
        try:
            with open(lock_file, 'w') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return lock
        except BlockingIOError:
            time.sleep(1)

def release_lock(lock):
    fcntl.flock(lock, fcntl.LOCK_UN)

def get_process_count():
    if not os.path.exists(counter_file):
        return 0
    with open(counter_file, 'r') as f:
        count = int(f.read())
    return count

def increment_process_count():
    count = get_process_count()
    with open(counter_file, 'w') as f:
        f.write(str(count + 1))

def decrement_process_count():
    count = get_process_count()
    with open(counter_file, 'w') as f:
        f.write(str(count - 1))

def start_process():
    pid = os.getpid()
    running_file = f"{pid}_{process_name}.running"
    lock = acquire_lock()
    try:
        while get_process_count() >= max_instances:
            time.sleep(1)
        increment_process_count()
        with open(running_file, 'w') as f:
            f.write("Running")
    finally:
        release_lock(lock)
    # Run your processA logic here
    time.sleep(10)  # Simulate processA running
    # Cleanup
    os.remove(running_file)
    lock = acquire_lock()
    try:
        decrement_process_count()
    finally:
        release_lock(lock)

if __name__ == "__main__":
    start_process()
