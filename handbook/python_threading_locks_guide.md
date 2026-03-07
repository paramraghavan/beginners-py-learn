# Python Threading & Locks - Complete Practical Guide

A comprehensive guide to the most common threading patterns and lock usage in Python (covering 90% of real-world use cases).

## Table of Contents
1. [Threading Basics](#threading-basics)
2. [Locks and Synchronization](#locks-and-synchronization)
3. [Common Patterns](#common-patterns)
4. [Real-World Examples](#real-world-examples)

---

## Threading Basics

### Simple Thread Creation

```python
import threading
import time

def worker(name: str, sleep_time: int):
    """Simple worker function"""
    print(f"Worker {name} starting")
    time.sleep(sleep_time)
    print(f"Worker {name} finished")

# Create and start threads
thread1 = threading.Thread(target=worker, args=("A", 2))
thread2 = threading.Thread(target=worker, args=("B", 1))

thread1.start()
thread2.start()

# Wait for threads to complete
thread1.join()
thread2.join()

print("All workers finished")
```

### Daemon Threads

```python
import threading
import time

def background_task():
    """Daemon thread that runs in background"""
    while True:
        print("Background task running...")
        time.sleep(2)

# Daemon thread - will be killed when main program exits
daemon = threading.Thread(target=background_task, daemon=True)
daemon.start()

time.sleep(5)
print("Main program ending - daemon will stop")
```

---

## Locks and Synchronization

### 1. Basic Lock (`threading.Lock`)

**Use Case:** Prevent race conditions when multiple threads access shared data.

```python
import threading

# Shared resource
counter = 0
lock = threading.Lock()

def increment_counter(num_iterations: int):
    global counter
    for _ in range(num_iterations):
        with lock:  # Acquire lock
            counter += 1
        # Lock automatically released

# Without lock - race condition
def unsafe_increment(num_iterations: int):
    global counter
    for _ in range(num_iterations):
        counter += 1  # UNSAFE!

# Safe usage
threads = [
    threading.Thread(target=increment_counter, args=(100000,))
    for _ in range(10)
]

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Final counter: {counter}")  # Will be 1,000,000
```

### 2. Reentrant Lock (`threading.RLock`)

**Use Case:** When same thread needs to acquire lock multiple times (recursive calls).

```python
import threading

class BankAccount:
    def __init__(self, balance: float):
        self.balance = balance
        self.lock = threading.RLock()  # Reentrant lock

    def withdraw(self, amount: float) -> bool:
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                return True
            return False

    def transfer_to(self, other: 'BankAccount', amount: float) -> bool:
        """Needs to acquire lock on both accounts"""
        with self.lock:  # Lock this account
            if self.withdraw(amount):  # Reacquires same lock - OK with RLock
                with other.lock:  # Lock other account
                    other.balance += amount
                return True
            return False

# Usage
account1 = BankAccount(1000)
account2 = BankAccount(500)

account1.transfer_to(account2, 200)
print(f"Account 1: ${account1.balance}")  # $800
print(f"Account 2: ${account2.balance}")  # $700
```

### 3. Semaphore

**Use Case:** Limit number of threads accessing a resource.

```python
import threading
import time

# Allow max 3 concurrent connections
semaphore = threading.Semaphore(3)

def access_database(thread_id: int):
    print(f"Thread {thread_id} waiting for database access...")

    with semaphore:
        print(f"Thread {thread_id} accessing database")
        time.sleep(2)  # Simulate work
        print(f"Thread {thread_id} done")

# Create 10 threads but only 3 can access at once
threads = [
    threading.Thread(target=access_database, args=(i,))
    for i in range(10)
]

for t in threads:
    t.start()
for t in threads:
    t.join()
```

### 4. Event

**Use Case:** Signal between threads.

```python
import threading
import time

# Event for signaling
ready_event = threading.Event()

def waiter():
    print("Waiter: Waiting for signal...")
    ready_event.wait()  # Block until event is set
    print("Waiter: Received signal! Starting work.")

def signaler():
    print("Signaler: Preparing...")
    time.sleep(3)
    print("Signaler: Ready! Sending signal.")
    ready_event.set()  # Signal waiting threads

# Start threads
t1 = threading.Thread(target=waiter)
t2 = threading.Thread(target=signaler)

t1.start()
t2.start()

t1.join()
t2.join()
```

### 5. Condition

**Use Case:** Wait for specific condition to be true.

```python
import threading
import time
from collections import deque

class DataQueue:
    def __init__(self):
        self.queue = deque()
        self.condition = threading.Condition()

    def put(self, item):
        with self.condition:
            self.queue.append(item)
            print(f"Added {item}, queue size: {len(self.queue)}")
            self.condition.notify()  # Wake up one waiting thread

    def get(self):
        with self.condition:
            while not self.queue:  # Wait until queue has items
                print("Queue empty, waiting...")
                self.condition.wait()
            item = self.queue.popleft()
            print(f"Got {item}, queue size: {len(self.queue)}")
            return item

# Usage
queue = DataQueue()

def consumer():
    for _ in range(5):
        item = queue.get()
        time.sleep(0.5)

def producer():
    for i in range(5):
        time.sleep(1)
        queue.put(f"item-{i}")

t1 = threading.Thread(target=consumer)
t2 = threading.Thread(target=producer)

t1.start()
t2.start()
t1.join()
t2.join()
```

---

## Common Patterns

### Pattern 1: Worker Queue (Most Common - 40% of use cases)

**Use Case:** Process multiple tasks with a fixed number of worker threads.

```python
import threading
import queue
import time
from typing import Callable, Any

class WorkerPool:
    def __init__(self, num_workers: int):
        self.task_queue = queue.Queue()
        self.workers = []
        self.running = True

        # Create worker threads
        for i in range(num_workers):
            worker = threading.Thread(target=self._worker, args=(i,))
            worker.start()
            self.workers.append(worker)

    def _worker(self, worker_id: int):
        """Worker thread that processes tasks from queue"""
        while self.running:
            try:
                # Get task with timeout so we can check self.running
                task, args, kwargs = self.task_queue.get(timeout=1)
                print(f"Worker {worker_id} processing task")

                try:
                    task(*args, **kwargs)
                except Exception as e:
                    print(f"Worker {worker_id} error: {e}")
                finally:
                    self.task_queue.task_done()
            except queue.Empty:
                continue

    def submit(self, task: Callable, *args, **kwargs):
        """Add task to queue"""
        self.task_queue.put((task, args, kwargs))

    def wait_completion(self):
        """Wait for all tasks to complete"""
        self.task_queue.join()

    def shutdown(self):
        """Shutdown all workers"""
        self.running = False
        for worker in self.workers:
            worker.join()

# Example usage
def download_file(url: str):
    print(f"Downloading {url}")
    time.sleep(2)  # Simulate download
    print(f"Completed {url}")

# Create pool with 3 workers
pool = WorkerPool(num_workers=3)

# Submit tasks
urls = [f"http://example.com/file{i}.zip" for i in range(10)]
for url in urls:
    pool.submit(download_file, url)

# Wait for all downloads
pool.wait_completion()
pool.shutdown()
print("All downloads complete")
```

### Pattern 2: Producer-Consumer (20% of use cases)

**Use Case:** One or more threads produce data, others consume it.

```python
import threading
import queue
import time
import random

def producer(q: queue.Queue, producer_id: int, num_items: int):
    """Produce items and put in queue"""
    for i in range(num_items):
        item = f"P{producer_id}-Item{i}"
        q.put(item)
        print(f"Producer {producer_id} produced: {item}")
        time.sleep(random.uniform(0.1, 0.5))

    print(f"Producer {producer_id} finished")

def consumer(q: queue.Queue, consumer_id: int, stop_event: threading.Event):
    """Consume items from queue"""
    while not stop_event.is_set():
        try:
            item = q.get(timeout=1)
            print(f"  Consumer {consumer_id} consumed: {item}")
            time.sleep(random.uniform(0.1, 0.3))  # Process item
            q.task_done()
        except queue.Empty:
            continue

    print(f"Consumer {consumer_id} stopped")

# Setup
work_queue = queue.Queue(maxsize=10)  # Limited queue size
stop_event = threading.Event()

# Create 2 producers, 3 consumers
producers = [
    threading.Thread(target=producer, args=(work_queue, i, 5))
    for i in range(2)
]

consumers = [
    threading.Thread(target=consumer, args=(work_queue, i, stop_event))
    for i in range(3)
]

# Start all threads
for p in producers:
    p.start()
for c in consumers:
    c.start()

# Wait for producers to finish
for p in producers:
    p.join()

# Wait for queue to be empty
work_queue.join()

# Stop consumers
stop_event.set()
for c in consumers:
    c.join()

print("All done!")
```

### Pattern 3: ThreadPoolExecutor (15% of use cases)

**Use Case:** Modern, high-level thread pool with futures.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def process_item(item: int) -> dict:
    """Process a single item"""
    print(f"Processing item {item}")
    time.sleep(1)
    return {"item": item, "result": item * 2}

# Using ThreadPoolExecutor (recommended modern approach)
items = list(range(10))

with ThreadPoolExecutor(max_workers=3) as executor:
    # Submit all tasks
    futures = [executor.submit(process_item, item) for item in items]

    # Process results as they complete
    for future in as_completed(futures):
        result = future.result()
        print(f"Got result: {result}")

# Alternative: map (preserves order)
with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(process_item, items)
    for result in results:
        print(f"Got result: {result}")
```

### Pattern 4: Thread-Safe Singleton (5% of use cases)

**Use Case:** Ensure only one instance of a class exists across threads.

```python
import threading

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Double-check locking
                if cls._instance is None:
                    print("Creating database connection...")
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize connection"""
        self.connection_id = id(self)
        print(f"Connection initialized: {self.connection_id}")

    def query(self, sql: str):
        print(f"Executing query on {self.connection_id}: {sql}")

# Test from multiple threads
def test_singleton(thread_id: int):
    db = DatabaseConnection()
    db.query(f"SELECT * FROM users WHERE id={thread_id}")

threads = [threading.Thread(target=test_singleton, args=(i,)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# All threads use same instance
```

### Pattern 5: Thread-Safe Counter/Metrics (10% of use cases)

**Use Case:** Track metrics across multiple threads.

```python
import threading
import time
from dataclasses import dataclass
from typing import Dict

@dataclass
class Metrics:
    success: int = 0
    failure: int = 0
    total: int = 0

class ThreadSafeMetrics:
    def __init__(self):
        self.metrics = Metrics()
        self.lock = threading.Lock()

    def record_success(self):
        with self.lock:
            self.metrics.success += 1
            self.metrics.total += 1

    def record_failure(self):
        with self.lock:
            self.metrics.failure += 1
            self.metrics.total += 1

    def get_stats(self) -> dict:
        with self.lock:
            return {
                'success': self.metrics.success,
                'failure': self.metrics.failure,
                'total': self.metrics.total,
                'success_rate': (
                    self.metrics.success / self.metrics.total * 100
                    if self.metrics.total > 0 else 0
                )
            }

# Usage
metrics = ThreadSafeMetrics()

def worker(worker_id: int):
    import random
    for _ in range(10):
        time.sleep(0.1)
        if random.random() > 0.3:
            metrics.record_success()
        else:
            metrics.record_failure()

threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

stats = metrics.get_stats()
print(f"Stats: {stats}")
```

### Pattern 6: Pipeline Pattern (Data Processing - 5% of use cases)

**Use Case:** Chain of processing stages where output of one stage is input to next.

```python
import threading
import queue
import time
from typing import Any, Callable

class PipelineStage:
    """A single stage in the pipeline"""

    def __init__(self, name: str, process_func: Callable, num_workers: int = 2):
        self.name = name
        self.process_func = process_func
        self.input_queue = queue.Queue(maxsize=20)
        self.output_queue = None  # Set when connecting stages
        self.workers = []
        self.running = False
        self.num_workers = num_workers

    def _worker(self):
        """Worker that processes items"""
        while self.running:
            try:
                item = self.input_queue.get(timeout=1)
                if item is None:  # Poison pill
                    break

                # Process the item
                try:
                    result = self.process_func(item)

                    # Pass to next stage
                    if self.output_queue:
                        self.output_queue.put(result)
                except Exception as e:
                    print(f"Error in {self.name}: {e}")
                finally:
                    self.input_queue.task_done()
            except queue.Empty:
                continue

    def start(self):
        """Start workers"""
        self.running = True
        for i in range(self.num_workers):
            worker = threading.Thread(
                target=self._worker,
                name=f"{self.name}-Worker-{i}"
            )
            worker.start()
            self.workers.append(worker)

    def stop(self):
        """Stop workers"""
        self.running = False
        # Send poison pills
        for _ in range(self.num_workers):
            self.input_queue.put(None)

        for worker in self.workers:
            worker.join()

    def connect(self, next_stage: 'PipelineStage'):
        """Connect this stage to the next"""
        self.output_queue = next_stage.input_queue

class Pipeline:
    """Multi-stage processing pipeline"""

    def __init__(self):
        self.stages = []

    def add_stage(self, name: str, process_func: Callable, num_workers: int = 2):
        """Add a processing stage"""
        stage = PipelineStage(name, process_func, num_workers)

        # Connect to previous stage
        if self.stages:
            self.stages[-1].connect(stage)

        self.stages.append(stage)
        return self

    def start(self):
        """Start all stages"""
        for stage in self.stages:
            stage.start()

    def stop(self):
        """Stop all stages"""
        for stage in self.stages:
            stage.stop()

    def input(self, item: Any):
        """Add item to pipeline"""
        if self.stages:
            self.stages[0].input_queue.put(item)

    def get_output_queue(self) -> queue.Queue:
        """Get output queue of last stage"""
        if self.stages:
            # Create final output queue
            output_queue = queue.Queue()
            self.stages[-1].output_queue = output_queue
            return output_queue
        return None

# Example: Image processing pipeline
def load_image(filename: str) -> dict:
    """Stage 1: Load image"""
    print(f"Loading {filename}")
    time.sleep(0.1)
    return {"filename": filename, "data": "raw_image_data"}

def resize_image(image: dict) -> dict:
    """Stage 2: Resize"""
    print(f"Resizing {image['filename']}")
    time.sleep(0.2)
    image["resized"] = True
    return image

def apply_filter(image: dict) -> dict:
    """Stage 3: Apply filter"""
    print(f"Filtering {image['filename']}")
    time.sleep(0.15)
    image["filtered"] = True
    return image

def save_image(image: dict) -> str:
    """Stage 4: Save"""
    print(f"Saving {image['filename']}")
    time.sleep(0.1)
    return f"processed_{image['filename']}"

# Build and run pipeline
pipeline = Pipeline()
pipeline.add_stage("Load", load_image, num_workers=2)
pipeline.add_stage("Resize", resize_image, num_workers=3)
pipeline.add_stage("Filter", apply_filter, num_workers=3)
pipeline.add_stage("Save", save_image, num_workers=2)

output_queue = pipeline.get_output_queue()
pipeline.start()

# Feed images to pipeline
images = [f"image{i}.jpg" for i in range(10)]
for img in images:
    pipeline.input(img)

# Collect results
time.sleep(5)  # Wait for processing
pipeline.stop()
```

### Pattern 7: Priority Queue Pattern (5% of use cases)

**Use Case:** Process high-priority tasks before low-priority ones.

```python
import threading
import queue
import time
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class PriorityTask:
    """Task with priority (lower number = higher priority)"""
    priority: int
    task_id: str
    func: Callable
    args: tuple = ()
    kwargs: dict = None

    def __lt__(self, other):
        return self.priority < other.priority

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}

class PriorityWorkerPool:
    """Worker pool that processes tasks by priority"""

    def __init__(self, num_workers: int = 3):
        self.task_queue = queue.PriorityQueue()
        self.num_workers = num_workers
        self.workers = []
        self.running = False
        self.results = []
        self.results_lock = threading.Lock()

    def _worker(self, worker_id: int):
        """Worker thread"""
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
                if task is None:  # Poison pill
                    break

                print(f"Worker {worker_id} processing {task.task_id} (priority {task.priority})")

                try:
                    result = task.func(*task.args, **task.kwargs)
                    with self.results_lock:
                        self.results.append({
                            'task_id': task.task_id,
                            'priority': task.priority,
                            'result': result
                        })
                except Exception as e:
                    print(f"Error in task {task.task_id}: {e}")
                finally:
                    self.task_queue.task_done()
            except queue.Empty:
                continue

    def start(self):
        """Start workers"""
        self.running = True
        for i in range(self.num_workers):
            worker = threading.Thread(target=self._worker, args=(i,))
            worker.start()
            self.workers.append(worker)

    def submit(self, priority: int, task_id: str, func: Callable, *args, **kwargs):
        """Submit task with priority"""
        task = PriorityTask(priority, task_id, func, args, kwargs)
        self.task_queue.put(task)

    def wait_completion(self):
        """Wait for all tasks"""
        self.task_queue.join()

    def shutdown(self):
        """Shutdown workers"""
        self.running = False
        for _ in range(self.num_workers):
            self.task_queue.put(None)

        for worker in self.workers:
            worker.join()

# Example usage
def process_request(request_id: str, request_type: str):
    """Process a request"""
    time.sleep(0.5)
    return f"Processed {request_type} request {request_id}"

pool = PriorityWorkerPool(num_workers=2)
pool.start()

# Submit tasks with different priorities
pool.submit(priority=5, task_id="req-1", func=process_request,
            request_id="1", request_type="normal")
pool.submit(priority=1, task_id="req-2", func=process_request,
            request_id="2", request_type="URGENT")
pool.submit(priority=5, task_id="req-3", func=process_request,
            request_id="3", request_type="normal")
pool.submit(priority=2, task_id="req-4", func=process_request,
            request_id="4", request_type="high")

pool.wait_completion()
pool.shutdown()

print("\nResults:")
for result in pool.results:
    print(f"  {result}")
```

### Pattern 8: Fan-Out/Fan-In Pattern (5% of use cases)

**Use Case:** Distribute work to multiple workers and collect results.

```python
import threading
import queue
import time
from typing import List, Callable, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

class FanOutFanIn:
    """Fan-out work to multiple workers, fan-in results"""

    def __init__(self, num_workers: int = 5):
        self.num_workers = num_workers

    def process(
        self,
        items: List[Any],
        process_func: Callable,
        aggregate_func: Callable = None
    ) -> Any:
        """
        Fan-out: distribute items to workers
        Fan-in: collect and optionally aggregate results
        """
        results = []
        results_lock = threading.Lock()

        def worker(item):
            result = process_func(item)
            with results_lock:
                results.append(result)
            return result

        # Fan-out: distribute to workers
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [executor.submit(worker, item) for item in items]

            # Fan-in: wait for all to complete
            for future in as_completed(futures):
                future.result()  # Ensure exceptions are raised

        # Optional aggregation
        if aggregate_func:
            return aggregate_func(results)

        return results

# Example 1: Parallel data fetching and aggregation
def fetch_user_data(user_id: int) -> dict:
    """Fetch data for one user"""
    print(f"Fetching user {user_id}")
    time.sleep(0.5)
    return {"user_id": user_id, "points": user_id * 10}

def aggregate_points(results: List[dict]) -> dict:
    """Aggregate all user points"""
    total = sum(r["points"] for r in results)
    return {
        "total_users": len(results),
        "total_points": total,
        "average_points": total / len(results)
    }

# Process
fan_out_fan_in = FanOutFanIn(num_workers=5)
user_ids = list(range(1, 11))

# Fan-out to fetch, fan-in to aggregate
summary = fan_out_fan_in.process(
    items=user_ids,
    process_func=fetch_user_data,
    aggregate_func=aggregate_points
)

print(f"\nSummary: {summary}")

# Example 2: MapReduce-style computation
def map_func(text: str) -> dict:
    """Map: count words in text"""
    words = text.lower().split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts

def reduce_func(word_counts: List[dict]) -> dict:
    """Reduce: combine all word counts"""
    total_counts = {}
    for counts in word_counts:
        for word, count in counts.items():
            total_counts[word] = total_counts.get(word, 0) + count
    return total_counts

texts = [
    "hello world",
    "hello python",
    "python is great",
    "world of python"
]

word_counts = fan_out_fan_in.process(
    items=texts,
    process_func=map_func,
    aggregate_func=reduce_func
)

print(f"\nWord counts: {word_counts}")
```

### Pattern 9: Barrier Pattern (Thread Synchronization - 3% of use cases)

**Use Case:** Synchronize multiple threads at a specific point.

```python
import threading
import time
import random

def multi_phase_task(barrier: threading.Barrier, worker_id: int):
    """Task with multiple phases that need synchronization"""

    # Phase 1: Initialization
    print(f"Worker {worker_id}: Initializing...")
    time.sleep(random.uniform(0.5, 1.5))
    print(f"Worker {worker_id}: Init done, waiting at barrier")

    barrier.wait()  # Wait for all workers to complete Phase 1

    # Phase 2: Processing (only starts when all workers are ready)
    print(f"Worker {worker_id}: Processing...")
    time.sleep(random.uniform(0.5, 1.5))
    print(f"Worker {worker_id}: Processing done, waiting at barrier")

    barrier.wait()  # Wait for all workers to complete Phase 2

    # Phase 3: Finalization
    print(f"Worker {worker_id}: Finalizing...")
    time.sleep(random.uniform(0.5, 1.5))
    print(f"Worker {worker_id}: All done!")

# Create barrier for 5 workers
num_workers = 5
barrier = threading.Barrier(num_workers)

# Start workers
threads = [
    threading.Thread(target=multi_phase_task, args=(barrier, i))
    for i in range(num_workers)
]

for t in threads:
    t.start()

for t in threads:
    t.join()

print("All workers completed all phases")
```

### Pattern 10: Thread-Local Storage (5% of use cases)

**Use Case:** Store data that's specific to each thread.

```python
import threading
import time
import random

# Thread-local storage
thread_local = threading.local()

def initialize_thread():
    """Initialize thread-local data"""
    thread_local.request_id = f"REQ-{threading.get_ident()}"
    thread_local.start_time = time.time()
    thread_local.counter = 0

def process_item(item: int):
    """Process item using thread-local data"""
    # Each thread has its own request_id and counter
    thread_local.counter += 1

    print(
        f"[{thread_local.request_id}] "
        f"Processing item {item} "
        f"(count: {thread_local.counter})"
    )

    time.sleep(random.uniform(0.1, 0.3))

def worker(worker_id: int, items: list):
    """Worker with thread-local storage"""
    # Initialize thread-local data for this thread
    initialize_thread()

    print(f"Worker {worker_id} started with request_id: {thread_local.request_id}")

    # Process items
    for item in items:
        process_item(item)

    # Report stats using thread-local data
    duration = time.time() - thread_local.start_time
    print(
        f"[{thread_local.request_id}] "
        f"Completed {thread_local.counter} items in {duration:.2f}s"
    )

# Start multiple workers
threads = []
for i in range(3):
    items = list(range(i * 5, (i + 1) * 5))
    t = threading.Thread(target=worker, args=(i, items))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

### Pattern 11: Batch Processing Pattern (5% of use cases)

**Use Case:** Accumulate items before processing in batches (more efficient).

```python
import threading
import queue
import time
from typing import List, Callable

class BatchProcessor:
    """Process items in batches for efficiency"""

    def __init__(
        self,
        batch_size: int = 10,
        max_wait_seconds: float = 2.0,
        num_workers: int = 2
    ):
        self.batch_size = batch_size
        self.max_wait_seconds = max_wait_seconds
        self.num_workers = num_workers

        self.item_queue = queue.Queue()
        self.batch_queue = queue.Queue()
        self.running = False

        self.batcher_thread = None
        self.worker_threads = []

    def _batcher(self):
        """Collect items into batches"""
        batch = []
        last_batch_time = time.time()

        while self.running:
            try:
                # Try to get item with short timeout
                item = self.item_queue.get(timeout=0.1)
                if item is None:  # Poison pill
                    break

                batch.append(item)

                # Send batch if full or timeout
                should_send = (
                    len(batch) >= self.batch_size or
                    (time.time() - last_batch_time) >= self.max_wait_seconds
                )

                if should_send and batch:
                    print(f"Sending batch of {len(batch)} items")
                    self.batch_queue.put(batch)
                    batch = []
                    last_batch_time = time.time()

            except queue.Empty:
                # Send partial batch if timeout
                if batch and (time.time() - last_batch_time) >= self.max_wait_seconds:
                    print(f"Timeout: Sending batch of {len(batch)} items")
                    self.batch_queue.put(batch)
                    batch = []
                    last_batch_time = time.time()

        # Send remaining items
        if batch:
            self.batch_queue.put(batch)

    def _worker(self, worker_id: int, process_func: Callable):
        """Process batches"""
        while self.running:
            try:
                batch = self.batch_queue.get(timeout=1)
                if batch is None:  # Poison pill
                    break

                print(f"Worker {worker_id} processing batch of {len(batch)}")
                process_func(batch)
                self.batch_queue.task_done()
            except queue.Empty:
                continue

    def start(self, process_func: Callable):
        """Start batcher and workers"""
        self.running = True

        # Start batcher thread
        self.batcher_thread = threading.Thread(target=self._batcher)
        self.batcher_thread.start()

        # Start worker threads
        for i in range(self.num_workers):
            worker = threading.Thread(target=self._worker, args=(i, process_func))
            worker.start()
            self.worker_threads.append(worker)

    def add_item(self, item):
        """Add item to be processed"""
        self.item_queue.put(item)

    def stop(self):
        """Stop processing"""
        # Stop batcher
        self.item_queue.put(None)
        self.batcher_thread.join()

        # Stop workers
        for _ in range(self.num_workers):
            self.batch_queue.put(None)

        for worker in self.worker_threads:
            worker.join()

        self.running = False

# Example: Batch database inserts
def bulk_insert(batch: List[dict]):
    """Insert batch of records"""
    print(f"  Inserting {len(batch)} records to database")
    time.sleep(0.5)  # Simulate database operation
    print(f"  Inserted: {[item['id'] for item in batch]}")

# Create processor
processor = BatchProcessor(
    batch_size=5,
    max_wait_seconds=2.0,
    num_workers=2
)

processor.start(process_func=bulk_insert)

# Add items one by one
for i in range(23):
    item = {"id": i, "data": f"record-{i}"}
    processor.add_item(item)
    time.sleep(0.2)  # Items arrive over time

time.sleep(3)  # Wait for processing
processor.stop()
```

### Pattern 12: Advanced Producer-Consumer with Multiple Queues

**Use Case:** Complex workflows with different types of producers and consumers.

```python
import threading
import queue
import time
import random
from enum import Enum
from dataclasses import dataclass
from typing import Any

class TaskType(Enum):
    URGENT = 1
    NORMAL = 2
    BATCH = 3

@dataclass
class Task:
    task_type: TaskType
    data: Any
    task_id: str

class MultiQueueSystem:
    """Producer-consumer with separate queues for different task types"""

    def __init__(self):
        # Separate queues for different task types
        self.urgent_queue = queue.Queue()
        self.normal_queue = queue.Queue()
        self.batch_queue = queue.Queue()

        self.running = False
        self.workers = []
        self.stats_lock = threading.Lock()
        self.stats = {TaskType.URGENT: 0, TaskType.NORMAL: 0, TaskType.BATCH: 0}

    def producer(self, producer_id: int, num_tasks: int):
        """Produce tasks of different types"""
        for i in range(num_tasks):
            # Random task type
            task_type = random.choice(list(TaskType))
            task = Task(
                task_type=task_type,
                data=f"Data-{i}",
                task_id=f"P{producer_id}-T{i}"
            )

            # Route to appropriate queue
            if task_type == TaskType.URGENT:
                self.urgent_queue.put(task)
            elif task_type == TaskType.NORMAL:
                self.normal_queue.put(task)
            else:
                self.batch_queue.put(task)

            print(f"Producer {producer_id} created {task_type.name} task {task.task_id}")
            time.sleep(random.uniform(0.1, 0.5))

    def consumer(self, consumer_id: int):
        """Consume tasks, prioritizing urgent tasks"""
        while self.running:
            task = None

            # Try queues in priority order
            try:
                task = self.urgent_queue.get_nowait()
            except queue.Empty:
                try:
                    task = self.normal_queue.get_nowait()
                except queue.Empty:
                    try:
                        task = self.batch_queue.get(timeout=1)
                    except queue.Empty:
                        continue

            if task:
                # Process task
                print(f"  Consumer {consumer_id} processing {task.task_type.name} task {task.task_id}")

                # Different processing times
                if task.task_type == TaskType.URGENT:
                    time.sleep(0.1)
                elif task.task_type == TaskType.NORMAL:
                    time.sleep(0.3)
                else:
                    time.sleep(0.5)

                # Update stats
                with self.stats_lock:
                    self.stats[task.task_type] += 1

                print(f"  Consumer {consumer_id} completed {task.task_id}")

    def start(self, num_producers: int = 2, num_consumers: int = 3, tasks_per_producer: int = 10):
        """Start the system"""
        self.running = True

        # Start producers
        producers = [
            threading.Thread(target=self.producer, args=(i, tasks_per_producer))
            for i in range(num_producers)
        ]

        # Start consumers
        consumers = [
            threading.Thread(target=self.consumer, args=(i,))
            for i in range(num_consumers)
        ]

        for p in producers:
            p.start()

        for c in consumers:
            c.start()

        # Wait for producers
        for p in producers:
            p.join()

        # Wait for queues to empty
        self.urgent_queue.join()
        self.normal_queue.join()
        self.batch_queue.join()

        # Stop consumers
        self.running = False
        for c in consumers:
            c.join()

        # Print stats
        print("\n=== Processing Stats ===")
        for task_type, count in self.stats.items():
            print(f"{task_type.name}: {count} tasks processed")

# Run the system
system = MultiQueueSystem()
system.start(num_producers=3, num_consumers=4, tasks_per_producer=5)
```

---

## Real-World Examples

### Example 1: Web Scraper with Thread Pool

```python
import threading
import queue
import time
import requests
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class ScrapedData:
    url: str
    status_code: int
    content_length: int
    error: str = None

class WebScraper:
    def __init__(self, num_workers: int = 5):
        self.task_queue = queue.Queue()
        self.results = []
        self.results_lock = threading.Lock()
        self.workers = []
        self.num_workers = num_workers

    def scrape_url(self, url: str) -> ScrapedData:
        """Scrape a single URL"""
        try:
            print(f"Scraping {url}")
            response = requests.get(url, timeout=10)
            return ScrapedData(
                url=url,
                status_code=response.status_code,
                content_length=len(response.content)
            )
        except Exception as e:
            return ScrapedData(
                url=url,
                status_code=0,
                content_length=0,
                error=str(e)
            )

    def _worker(self):
        """Worker thread function"""
        while True:
            try:
                url = self.task_queue.get(timeout=1)
                if url is None:  # Poison pill to stop worker
                    break

                result = self.scrape_url(url)

                with self.results_lock:
                    self.results.append(result)

                self.task_queue.task_done()
            except queue.Empty:
                continue

    def scrape_urls(self, urls: List[str]) -> List[ScrapedData]:
        """Scrape multiple URLs using thread pool"""
        # Start workers
        for _ in range(self.num_workers):
            worker = threading.Thread(target=self._worker)
            worker.start()
            self.workers.append(worker)

        # Add URLs to queue
        for url in urls:
            self.task_queue.put(url)

        # Wait for all tasks to complete
        self.task_queue.join()

        # Stop workers
        for _ in range(self.num_workers):
            self.task_queue.put(None)  # Poison pill

        for worker in self.workers:
            worker.join()

        return self.results

# Usage
scraper = WebScraper(num_workers=3)
urls = [
    'http://example.com',
    'http://example.org',
    'http://example.net',
    # Add more URLs
]

results = scraper.scrape_urls(urls)
for result in results:
    if result.error:
        print(f"ERROR {result.url}: {result.error}")
    else:
        print(f"SUCCESS {result.url}: {result.status_code}, {result.content_length} bytes")
```

### Example 2: File Processor with Progress Tracking

```python
import threading
import queue
from pathlib import Path
from typing import List, Callable
import time

class FileProcessor:
    def __init__(self, num_workers: int = 3):
        self.task_queue = queue.Queue()
        self.num_workers = num_workers
        self.processed_count = 0
        self.total_count = 0
        self.lock = threading.Lock()
        self.progress_callback = None

    def set_progress_callback(self, callback: Callable[[int, int], None]):
        """Set callback for progress updates"""
        self.progress_callback = callback

    def _update_progress(self):
        """Update progress counter"""
        with self.lock:
            self.processed_count += 1
            if self.progress_callback:
                self.progress_callback(self.processed_count, self.total_count)

    def _worker(self, process_func: Callable):
        """Worker thread"""
        while True:
            try:
                file_path = self.task_queue.get(timeout=1)
                if file_path is None:
                    break

                try:
                    process_func(file_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                finally:
                    self._update_progress()
                    self.task_queue.task_done()
            except queue.Empty:
                continue

    def process_files(self, files: List[Path], process_func: Callable):
        """Process multiple files with progress tracking"""
        self.total_count = len(files)
        self.processed_count = 0

        # Start workers
        workers = []
        for _ in range(self.num_workers):
            worker = threading.Thread(target=self._worker, args=(process_func,))
            worker.start()
            workers.append(worker)

        # Queue files
        for file_path in files:
            self.task_queue.put(file_path)

        # Wait for completion
        self.task_queue.join()

        # Stop workers
        for _ in range(self.num_workers):
            self.task_queue.put(None)

        for worker in workers:
            worker.join()

# Usage
def process_text_file(file_path: Path):
    """Process a single text file"""
    print(f"Processing {file_path.name}")
    content = file_path.read_text()
    # Do something with content
    time.sleep(0.5)  # Simulate processing

def progress_callback(processed: int, total: int):
    """Progress update callback"""
    percentage = (processed / total * 100) if total > 0 else 0
    print(f"Progress: {processed}/{total} ({percentage:.1f}%)")

# Process all text files in directory
processor = FileProcessor(num_workers=4)
processor.set_progress_callback(progress_callback)

files = list(Path(".").glob("*.txt"))
processor.process_files(files, process_text_file)
```

### Example 3: Rate-Limited API Client

```python
import threading
import time
from collections import deque
from typing import Callable, Any

class RateLimiter:
    """Rate limiter using token bucket algorithm"""

    def __init__(self, max_calls: int, time_window: float):
        """
        Args:
            max_calls: Maximum number of calls allowed
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
        self.lock = threading.Lock()

    def acquire(self):
        """Wait until a call is allowed"""
        with self.lock:
            now = time.time()

            # Remove old calls outside time window
            while self.calls and self.calls[0] <= now - self.time_window:
                self.calls.popleft()

            # Check if we can make a call
            if len(self.calls) >= self.max_calls:
                # Need to wait
                sleep_time = self.calls[0] + self.time_window - now
                time.sleep(sleep_time)
                # After sleep, remove old calls
                self.calls.popleft()

            # Record this call
            self.calls.append(time.time())

class RateLimitedAPIClient:
    def __init__(self, calls_per_second: int = 10):
        self.rate_limiter = RateLimiter(calls_per_second, 1.0)

    def api_call(self, endpoint: str, data: dict) -> dict:
        """Make rate-limited API call"""
        self.rate_limiter.acquire()

        print(f"Calling {endpoint} at {time.time():.2f}")
        # Simulate API call
        time.sleep(0.1)
        return {"status": "success", "data": data}

    def bulk_api_calls(self, requests: list, num_workers: int = 5):
        """Make multiple API calls with rate limiting"""
        results = []
        results_lock = threading.Lock()

        def worker():
            while True:
                try:
                    endpoint, data = request_queue.get(timeout=1)
                    result = self.api_call(endpoint, data)

                    with results_lock:
                        results.append(result)

                    request_queue.task_done()
                except:
                    break

        # Setup queue and workers
        import queue
        request_queue = queue.Queue()

        for req in requests:
            request_queue.put(req)

        workers = [threading.Thread(target=worker) for _ in range(num_workers)]
        for w in workers:
            w.start()

        request_queue.join()
        return results

# Usage
client = RateLimitedAPIClient(calls_per_second=5)

requests = [
    ("/users", {"id": i})
    for i in range(20)
]

start = time.time()
results = client.bulk_api_calls(requests, num_workers=3)
duration = time.time() - start

print(f"\nCompleted {len(results)} requests in {duration:.2f}s")
print(f"Rate: {len(results)/duration:.2f} requests/sec")
```

### Example 4: Cache with Thread-Safe Updates

```python
import threading
import time
from typing import Dict, Callable, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class CacheEntry:
    value: Any
    expires_at: datetime

class ThreadSafeCache:
    """Thread-safe cache with TTL"""

    def __init__(self, default_ttl_seconds: int = 300):
        self.cache: Dict[str, CacheEntry] = {}
        self.lock = threading.RLock()
        self.default_ttl = default_ttl_seconds
        self.stats = {'hits': 0, 'misses': 0}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                if datetime.now() < entry.expires_at:
                    self.stats['hits'] += 1
                    return entry.value
                else:
                    # Expired
                    del self.cache[key]

            self.stats['misses'] += 1
            return None

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None):
        """Set value in cache"""
        ttl = ttl_seconds or self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl)

        with self.lock:
            self.cache[key] = CacheEntry(value=value, expires_at=expires_at)

    def get_or_compute(
        self,
        key: str,
        compute_func: Callable[[], Any],
        ttl_seconds: Optional[int] = None
    ) -> Any:
        """Get from cache or compute if missing"""
        # Try to get from cache
        value = self.get(key)
        if value is not None:
            return value

        # Not in cache, compute value
        # Use lock to prevent multiple threads computing same value
        with self.lock:
            # Double-check - another thread might have computed it
            value = self.get(key)
            if value is not None:
                return value

            # Compute and cache
            value = compute_func()
            self.set(key, value, ttl_seconds)
            return value

    def clear_expired(self):
        """Remove expired entries"""
        with self.lock:
            now = datetime.now()
            expired_keys = [
                key for key, entry in self.cache.items()
                if now >= entry.expires_at
            ]
            for key in expired_keys:
                del self.cache[key]

    def get_stats(self) -> dict:
        """Get cache statistics"""
        with self.lock:
            total = self.stats['hits'] + self.stats['misses']
            hit_rate = (self.stats['hits'] / total * 100) if total > 0 else 0
            return {
                'size': len(self.cache),
                'hits': self.stats['hits'],
                'misses': self.stats['misses'],
                'hit_rate': f"{hit_rate:.1f}%"
            }

# Usage
cache = ThreadSafeCache(default_ttl_seconds=5)

def expensive_computation(item_id: int) -> str:
    """Simulate expensive operation"""
    print(f"Computing result for item {item_id}...")
    time.sleep(1)  # Expensive!
    return f"Result for item {item_id}"

def worker(thread_id: int, item_id: int):
    """Worker that uses cache"""
    result = cache.get_or_compute(
        key=f"item_{item_id}",
        compute_func=lambda: expensive_computation(item_id)
    )
    print(f"Thread {thread_id} got: {result}")

# Multiple threads accessing same items
threads = []
for i in range(10):
    # Multiple threads will request same items
    item_id = i % 3  # Only 3 unique items
    t = threading.Thread(target=worker, args=(i, item_id))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"\nCache stats: {cache.get_stats()}")
# Only 3 computations for 10 requests!
```

### Example 5: Background Job Scheduler

```python
import threading
import time
from datetime import datetime, timedelta
from typing import Callable, Optional
from dataclasses import dataclass
import queue

@dataclass
class ScheduledJob:
    name: str
    func: Callable
    interval_seconds: float
    next_run: datetime
    args: tuple = ()
    kwargs: dict = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}

class JobScheduler:
    """Background job scheduler with thread pool"""

    def __init__(self, num_workers: int = 3):
        self.jobs: list[ScheduledJob] = []
        self.jobs_lock = threading.Lock()
        self.task_queue = queue.Queue()
        self.running = False
        self.num_workers = num_workers
        self.scheduler_thread: Optional[threading.Thread] = None
        self.workers: list[threading.Thread] = []

    def add_job(
        self,
        name: str,
        func: Callable,
        interval_seconds: float,
        *args,
        **kwargs
    ):
        """Add a recurring job"""
        job = ScheduledJob(
            name=name,
            func=func,
            interval_seconds=interval_seconds,
            next_run=datetime.now(),
            args=args,
            kwargs=kwargs
        )

        with self.jobs_lock:
            self.jobs.append(job)

        print(f"Added job: {name} (runs every {interval_seconds}s)")

    def _worker(self, worker_id: int):
        """Worker thread that executes jobs"""
        while self.running:
            try:
                job = self.task_queue.get(timeout=1)
                print(f"Worker {worker_id} executing: {job.name}")

                try:
                    job.func(*job.args, **job.kwargs)
                except Exception as e:
                    print(f"Error in job {job.name}: {e}")

                self.task_queue.task_done()
            except queue.Empty:
                continue

    def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.running:
            now = datetime.now()

            with self.jobs_lock:
                for job in self.jobs:
                    if now >= job.next_run:
                        # Time to run this job
                        self.task_queue.put(job)
                        # Schedule next run
                        job.next_run = now + timedelta(seconds=job.interval_seconds)

            time.sleep(0.1)  # Check every 100ms

    def start(self):
        """Start the scheduler"""
        if self.running:
            return

        self.running = True

        # Start worker threads
        for i in range(self.num_workers):
            worker = threading.Thread(target=self._worker, args=(i,))
            worker.start()
            self.workers.append(worker)

        # Start scheduler thread
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self.scheduler_thread.start()

        print(f"Scheduler started with {self.num_workers} workers")

    def stop(self):
        """Stop the scheduler"""
        if not self.running:
            return

        self.running = False

        # Wait for scheduler thread
        if self.scheduler_thread:
            self.scheduler_thread.join()

        # Wait for queue to empty
        self.task_queue.join()

        # Stop workers
        for worker in self.workers:
            worker.join()

        print("Scheduler stopped")

# Usage example
def backup_database():
    print(f"[{datetime.now()}] Running database backup...")
    time.sleep(1)

def cleanup_logs():
    print(f"[{datetime.now()}] Cleaning up old logs...")
    time.sleep(0.5)

def send_reports():
    print(f"[{datetime.now()}] Sending reports...")
    time.sleep(0.8)

# Create scheduler
scheduler = JobScheduler(num_workers=2)

# Add jobs
scheduler.add_job("Database Backup", backup_database, interval_seconds=5)
scheduler.add_job("Log Cleanup", cleanup_logs, interval_seconds=3)
scheduler.add_job("Send Reports", send_reports, interval_seconds=7)

# Run for 20 seconds
scheduler.start()
time.sleep(20)
scheduler.stop()
```

---

## Best Practices

### 1. Always Use Context Managers for Locks

```python
# GOOD - automatic release
with lock:
    shared_data += 1

# BAD - manual release (can forget, or exception prevents release)
lock.acquire()
shared_data += 1
lock.release()
```

### 2. Avoid Global Variables with Threads

```python
# BAD - global variable
counter = 0
lock = threading.Lock()

# GOOD - encapsulate in class
class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1
```

### 3. Use Queue for Thread Communication

```python
# GOOD - thread-safe queue
import queue
task_queue = queue.Queue()

# BAD - shared list with manual locking
tasks = []
tasks_lock = threading.Lock()
```

### 4. Set Thread Names for Debugging

```python
def worker():
    print(f"Running in thread: {threading.current_thread().name}")
    # ... work

thread = threading.Thread(target=worker, name="MyWorker-1")
thread.start()
```

### 5. Use ThreadPoolExecutor for Simple Cases

```python
# GOOD - simple and clean
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(process_item, items)

# UNNECESSARY - manual thread management for simple tasks
threads = [threading.Thread(target=process_item, args=(item,)) for item in items]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

### 6. Always Clean Up Resources

```python
def worker():
    try:
        # Do work
        pass
    finally:
        # Clean up resources
        cleanup()

# Or use context managers
with resource:
    # Use resource
    pass
```

### 7. Avoid Deadlocks with Lock Ordering

```python
# BAD - can deadlock
def transfer(from_account, to_account, amount):
    with from_account.lock:
        with to_account.lock:
            # Transfer
            pass

# GOOD - consistent lock ordering
def transfer(from_account, to_account, amount):
    accounts = sorted([from_account, to_account], key=id)
    with accounts[0].lock:
        with accounts[1].lock:
            # Transfer
            pass
```

---

## Common Pitfalls

### 1. GIL (Global Interpreter Lock)

Python's GIL means only one thread executes Python bytecode at a time.

```python
# Threading is GOOD for I/O-bound tasks
def download_file(url):  # Waiting for network - releases GIL
    response = requests.get(url)
    return response.content

# Threading is BAD for CPU-bound tasks
def calculate_prime(n):  # Pure Python computation - holds GIL
    # Use multiprocessing instead!
    pass
```

### 2. Race Conditions

```python
# BAD - race condition
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1  # Not atomic! Read-modify-write

# GOOD - protected with lock
class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1
```

### 3. Forgetting to Join Threads

```python
# BAD - main program exits, threads abandoned
thread = threading.Thread(target=worker)
thread.start()
# Program ends, thread may not finish

# GOOD - wait for thread
thread = threading.Thread(target=worker)
thread.start()
thread.join()  # Wait for completion
```

---

## Quick Reference

| Use Case | Pattern | Key Components |
|----------|---------|----------------|
| Process multiple items concurrently | Worker Queue | `Queue`, `threading.Thread` |
| Protect shared data | Lock | `threading.Lock`, `with` statement |
| Limit concurrent access | Semaphore | `threading.Semaphore` |
| Signal between threads | Event | `threading.Event` |
| Wait for condition | Condition | `threading.Condition` |
| Modern thread pool | Executor | `concurrent.futures.ThreadPoolExecutor` |
| Producer-Consumer | Queue + Threads | `queue.Queue`, multiple threads |
| Singleton | Double-check locking | `threading.Lock`, `__new__` |
| Chain of processing stages | Pipeline | Multiple queues, chained stages |
| Priority-based processing | Priority Queue | `queue.PriorityQueue` |
| Distribute and collect work | Fan-Out/Fan-In | `ThreadPoolExecutor`, aggregation |
| Synchronize at checkpoint | Barrier | `threading.Barrier` |
| Thread-specific data | Thread-Local Storage | `threading.local()` |
| Batch processing | Batch Processor | Queue batching, timeout |
| Multiple task types | Multi-Queue | Separate queues per priority |

---

## Performance Tips

1. **Use ThreadPoolExecutor** for simple parallel tasks
2. **Use queues** for thread communication (thread-safe)
3. **Minimize lock contention** - keep critical sections small
4. **Use local variables** when possible (thread-local by default)
5. **Consider async/await** for I/O-bound tasks (asyncio)
6. **Use multiprocessing** for CPU-bound tasks (avoids GIL)

---

## Summary

**Most Common Patterns (95% of use cases):**

### Core Patterns (75%)
1. **Worker Queue Pattern (40%)** - Process tasks with thread pool
2. **Producer-Consumer (20%)** - Generate and process data
3. **ThreadPoolExecutor (15%)** - Modern high-level threading

### Data Protection & Synchronization (15%)
4. **Thread-Safe Data Structures (10%)** - Shared counters, caches, metrics
5. **Semaphore for Resource Limiting (5%)** - Control concurrent access

### Advanced Patterns (20%)
6. **Pipeline Pattern (5%)** - Chain of processing stages
7. **Priority Queue (5%)** - Priority-based task processing
8. **Fan-Out/Fan-In (5%)** - Parallel distribution and aggregation
9. **Batch Processing (5%)** - Efficient batched operations
10. **Thread-Local Storage (5%)** - Thread-specific data
11. **Barrier Pattern (3%)** - Multi-phase synchronization
12. **Multi-Queue Producer-Consumer (2%)** - Complex workflows

### When to Use Each Pattern

| Pattern | Best For |
|---------|----------|
| **Worker Queue** | Fixed workers, unlimited tasks (web scraping, file processing) |
| **Producer-Consumer** | Continuous data generation/consumption (log processing, streaming) |
| **ThreadPoolExecutor** | Simple parallel operations (API calls, quick tasks) |
| **Pipeline** | Multi-stage data processing (ETL, image/video processing) |
| **Priority Queue** | Tasks with different urgencies (request handling, job scheduling) |
| **Fan-Out/Fan-In** | Parallel computation + aggregation (MapReduce, data analysis) |
| **Batch Processing** | Efficiency through batching (database inserts, API bulk operations) |
| **Thread-Local** | Per-thread state (request IDs, connections, context) |
| **Barrier** | Synchronized phases (parallel algorithms, checkpointing) |

**Key Takeaway:**
- Start simple: Use `ThreadPoolExecutor` for basic parallelism
- Need queuing: Use Worker Queue or Producer-Consumer
- Complex workflows: Consider Pipeline or Multi-Queue patterns
- Always protect shared state with locks
- Always clean up resources

---

## Choosing the Right Pattern - Decision Tree

```
Do you need threading?
├─ YES, I/O-bound tasks (network, files, databases)
│   │
│   ├─ Simple parallel operations?
│   │   └─> Use ThreadPoolExecutor ✓
│   │
│   ├─ Fixed workers processing many tasks?
│   │   └─> Use Worker Queue Pattern ✓
│   │
│   ├─ Continuous data generation + consumption?
│   │   └─> Use Producer-Consumer Pattern ✓
│   │
│   ├─ Multi-stage processing?
│   │   └─> Use Pipeline Pattern ✓
│   │
│   ├─ Tasks have different priorities?
│   │   └─> Use Priority Queue Pattern ✓
│   │
│   ├─ Distribute work and aggregate results?
│   │   └─> Use Fan-Out/Fan-In Pattern ✓
│   │
│   ├─ More efficient to process in batches?
│   │   └─> Use Batch Processing Pattern ✓
│   │
│   └─ Threads need synchronized checkpoints?
│       └─> Use Barrier Pattern ✓
│
└─ NO, CPU-bound tasks (computation, data processing)
    └─> Use multiprocessing instead! ✓

Need to protect shared data?
├─ Simple counter or flag → threading.Lock
├─ Recursive locking needed → threading.RLock
├─ Limit concurrent access → threading.Semaphore
├─ Signal between threads → threading.Event
├─ Wait for condition → threading.Condition
└─ Thread-specific data → threading.local()
```

### Common Scenarios

**Scenario: Web Scraping 100 URLs**
```python
# Best choice: ThreadPoolExecutor (simple, clean)
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(scrape_url, urls)
```

**Scenario: Process 10,000 Files**
```python
# Best choice: Worker Queue (efficient, controlled)
pool = WorkerPool(num_workers=5)
for file in files:
    pool.submit(process_file, file)
pool.wait_completion()
pool.shutdown()
```

**Scenario: Real-time Log Processing**
```python
# Best choice: Producer-Consumer (continuous)
# Producer: reads logs
# Consumers: parse, analyze, store
```

**Scenario: Image Pipeline (load→resize→filter→save)**
```python
# Best choice: Pipeline Pattern (multi-stage)
pipeline.add_stage("Load", load_image)
pipeline.add_stage("Resize", resize)
pipeline.add_stage("Filter", apply_filter)
pipeline.add_stage("Save", save_image)
```

**Scenario: Database Bulk Inserts**
```python
# Best choice: Batch Processing (efficiency)
# Collect 100 records, then insert batch
batch_processor = BatchProcessor(batch_size=100)
```

**Scenario: Request Handling (critical vs normal)**
```python
# Best choice: Priority Queue (urgency)
pool.submit(priority=1, task=critical_request)
pool.submit(priority=5, task=normal_request)
```
