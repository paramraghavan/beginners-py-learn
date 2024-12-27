# Advanced Python Concurrency: A Teaching Guide

## Module 1: Understanding the Global Interpreter Lock (GIL)

### Lesson 1: The GIL Fundamentals

The Global Interpreter Lock is fundamental to understanding Python's concurrency model. Let's start with an example
that illustrates the GIL's impact:

```python
import time
import threading


def cpu_bound_task():
    """
    A CPU-intensive task that performs mathematical calculations.
    This type of task is heavily affected by the GIL.
    """
    start = time.perf_counter()
    result = 0
    for i in range(20_000_000):
        result += i * i
    end = time.perf_counter()
    print(f"Task completed in {end - start:.2f} seconds")


# First, let's run it in a single thread
print("Running in single thread...")
cpu_bound_task()

# Now, let's try running two instances simultaneously
print("\nRunning in two threads...")
t1 = threading.Thread(target=cpu_bound_task)
t2 = threading.Thread(target=cpu_bound_task)
t1.start()
t2.start()
t1.join()
t2.join()
```

Notes:

1. Run this code and observe that the two-threaded version doesn't run faster
2. Explain how the GIL prevents true parallel execution of Python bytecode
3. Discuss why CPython needs the GIL (reference counting, memory management)

### Lesson 2: GIL and I/O Operations

Let's contrast the previous example with I/O-bound tasks:

```python
import threading
import time
import requests


def io_bound_task():
    """
    An I/O-bound task that makes HTTP requests.
    The GIL is released during I/O operations.
    """
    start = time.perf_counter()
    for _ in range(5):
        response = requests.get('https://api.github.com')
        # Process response
    end = time.perf_counter()
    print(f"Task completed in {end - start:.2f} seconds")


# Single thread execution
print("Running in single thread...")
io_bound_task()

# Multi-threaded execution
print("\nRunning in multiple threads...")
threads = [threading.Thread(target=io_bound_task) for _ in range(3)]
[t.start() for t in threads]
[t.join() for t in threads]
```

Notes:

1. Demonstrate how I/O-bound tasks benefit from threading despite the GIL
2. Explain when Python releases the GIL
3. Discuss real-world scenarios where threading is beneficial

## Module 2: Working Around the GIL

### Lesson 1: Multiprocessing for CPU-Bound Tasks

Here's how to effectively parallelize CPU-intensive work:

```python
from multiprocessing import Pool
import time


def complex_calculation(range_start):
    """
    A CPU-intensive calculation that can be parallelized.
    """
    result = 0
    for i in range(range_start, range_start + 5_000_000):
        result += i * i
    return result


def demonstrate_multiprocessing():
    start = time.perf_counter()

    # Using multiple processes to perform calculations
    with Pool(processes=4) as pool:
        ranges = [i * 5_000_000 for i in range(4)]
        results = pool.map(complex_calculation, ranges)
        total = sum(results)

    end = time.perf_counter()
    print(f"Multiprocessing completed in {end - start:.2f} seconds")
    return total


# Compare with single-process version
def single_process():
    start = time.perf_counter()
    total = sum(complex_calculation(i * 5_000_000) for i in range(4))
    end = time.perf_counter()
    print(f"Single process completed in {end - start:.2f} seconds")
    return total


# Run both versions and compare results
single_result = single_process()
multi_result = demonstrate_multiprocessing()
assert single_result == multi_result, "Results don't match!"
```

Notes:

1. Explain process isolation and memory independence
2. Discuss the overhead of process creation and data serialization
3. Show how to choose the optimal number of processes

### Lesson 2: Advanced Process Pool Patterns

```python
from multiprocessing import Pool
from contextlib import contextmanager
import time


class ProcessPoolManager:
    """
    A context manager for handling process pools with error handling
    and resource cleanup.
    """

    def __init__(self, processes=None, initializer=None, initargs=None):
        self.processes = processes
        self.initializer = initializer
        self.initargs = initargs or ()
        self.pool = None

    def __enter__(self):
        self.pool = Pool(
            processes=self.processes,
            initializer=self.initializer,
            initargs=self.initargs
        )
        return self.pool

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pool:
            self.pool.close()
            if exc_type is None:
                self.pool.join()
            else:
                self.pool.terminate()
        return False


def initialize_worker():
    """
    Initialization function for worker processes.
    """
    print(f"Initializing worker process...")


def cpu_intensive_task(data):
    """
    Example task that benefits from multiprocessing.
    """
    time.sleep(1)  # Simulate complex computation
    return sum(x * x for x in range(data * 1000, (data + 1) * 1000))


# Usage example
def main():
    data = list(range(20))

    with ProcessPoolManager(processes=4, initializer=initialize_worker) as pool:
        try:
            results = pool.map(cpu_intensive_task, data)
            print(f"Processed {len(results)} tasks successfully")
        except Exception as e:
            print(f"Error during processing: {e}")
```

Notes:

1. Show proper resource management with context managers
2. Demonstrate worker initialization and cleanup
3. Explain error handling in multiprocessing contexts

## Module 3: Thread Safety and Synchronization

### Lesson 1: Thread Safety Patterns

```python
import threading
from typing import Dict, Any
from contextlib import contextmanager


class ThreadSafeDict:
    """
    A thread-safe dictionary implementation using a lock.
    Demonstrates proper synchronization patterns.
    """

    def __init__(self):
        self._dict: Dict[str, Any] = {}
        self._lock = threading.RLock()

    @contextmanager
    def _locked_operation(self):
        """Context manager for lock handling"""
        self._lock.acquire()
        try:
            yield
        finally:
            self._lock.release()

    def get(self, key: str, default: Any = None) -> Any:
        with self._locked_operation():
            return self._dict.get(key, default)

    def set(self, key: str, value: Any) -> None:
        with self._locked_operation():
            self._dict[key] = value

    def update(self, other: Dict[str, Any]) -> None:
        with self._locked_operation():
            self._dict.update(other)

    def __str__(self) -> str:
        with self._locked_operation():
            return str(self._dict)


# Usage demonstration
def worker(d: ThreadSafeDict, key: str):
    """Worker function to test thread safety"""
    for i in range(1000):
        current = d.get(key, 0)
        d.set(key, current + 1)


def demonstrate_thread_safety():
    d = ThreadSafeDict()
    threads = []

    # Create multiple threads updating the same key
    for _ in range(10):
        t = threading.Thread(target=worker, args=(d, 'counter'))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Verify the result
    print(f"Final counter value: {d.get('counter')}")
```

Notes:

1. Explain the importance of proper synchronization
2. Demonstrate the use of context managers for lock handling
3. Show how to verify thread safety through testing

### Lesson 2: Advanced Synchronization Patterns

```python
import threading
import queue
import time
from typing import Optional, List


class ThreadPool:
    """
    A custom thread pool implementation demonstrating advanced
    synchronization patterns.
    """

    def __init__(self, num_threads: int):
        self.tasks: queue.Queue = queue.Queue()
        self.results: List[Any] = []
        self.threads: List[threading.Thread] = []
        self._lock = threading.Lock()
        self._shutdown = threading.Event()

        # Initialize worker threads
        for _ in range(num_threads):
            thread = threading.Thread(target=self._worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def _worker(self) -> None:
        """Worker thread function"""
        while not self._shutdown.is_set():
            try:
                # Get task with timeout to check shutdown periodically
                task = self.tasks.get(timeout=0.1)
            except queue.Empty:
                continue

            try:
                result = task()
                with self._lock:
                    self.results.append(result)
            except Exception as e:
                print(f"Error in worker thread: {e}")
            finally:
                self.tasks.task_done()

    def submit(self, task: callable) -> None:
        """Submit a task to the thread pool"""
        if self._shutdown.is_set():
            raise RuntimeError("Cannot submit after shutdown")
        self.tasks.put(task)

    def shutdown(self) -> None:
        """Shutdown the thread pool"""
        self._shutdown.set()
        for thread in self.threads:
            thread.join()
```

Notes:

1. Demonstrate complex synchronization with multiple primitives
2. Show proper shutdown handling
3. Explain task queuing and result collection

## Module 4: Performance Analysis and Optimization

### Lesson 1: Profiling Concurrent Code

```python
import cProfile
import threading
import time
from typing import List, Optional


def profile_threads(target: callable, num_threads: int) -> None:
    """
    Profile multiple threads running the same target function.
    """
    profiler = cProfile.Profile()
    threads: List[threading.Thread] = []

    def wrapped_target():
        profiler.enable()
        target()
        profiler.disable()

    # Create and start threads
    for _ in range(num_threads):
        thread = threading.Thread(target=wrapped_target)
        threads.append(thread)
        thread.start()

    # Wait for completion
    for thread in threads:
        thread.join()

    # Print profiling results
    profiler.print_stats(sort='cumulative')


# Example usage
def cpu_bound_work():
    """Example function to profile"""
    result = 0
    for i in range(1_000_000):
        result += i * i
    return result


# Profile the execution
profile_threads(cpu_bound_work, 4)
```

Notes:

1. Show how to profile concurrent code
2. Demonstrate performance bottleneck identification
3. Explain profiling output interpretation

## Practical Exercises and Assignments

1. Task Queue Implementation:
    - Create a thread-safe task queue with priority support
    - Implement worker pools with different processing strategies
    - Add monitoring and metrics collection

2. Data Processing Pipeline:
    - Build a concurrent pipeline for processing large datasets
    - Implement both thread and process-based approaches
    - Compare performance characteristics

3. Real-world Application:
    - Create a web crawler using different concurrency models
    - Implement proper resource management and error handling
    - Add performance monitoring and optimization