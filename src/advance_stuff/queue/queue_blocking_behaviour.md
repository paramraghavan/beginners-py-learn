# Queue and its Blocking Behaviour
Both `queue.put()` and `queue.get()` are blocking operations by default and used very well with producer/consumer pattern 
1. `queue.put(item)` will block when the queue is full (if it has a maxsize)
2. `queue.get()` will block when the queue is empty
3  `queue.put_nowait(item)` non block when the queue is full will raise exception queue full
4. `queue.get_nowait()` non-block when the queue is empty raise exception queue empty

## Example

```python
import threading
import queue
import time
import logging
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)

# [dataclass-usage.md](../dataclass/dataclass-usage.md)
@dataclass
class Task:
    id: int
    created_at: datetime = datetime.now()


class Producer(threading.Thread):
    def __init__(self, task_queue: queue.Queue, max_tasks: int):
        super().__init__(name="Producer")
        self.queue = task_queue
        self.max_tasks = max_tasks

    def run(self):
        for i in range(self.max_tasks):
            task = Task(id=i)

            logging.info(f"Attempting to put task {i} into queue...")
            # This will block if queue is full
            self.queue.put(task)
            logging.info(f"Successfully added task {i} to queue")

            time.sleep(0.5)  # Simulate some work


class Consumer(threading.Thread):
    def __init__(self, task_queue: queue.Queue, process_time: float):
        super().__init__(name="Consumer")
        self.queue = task_queue
        self.process_time = process_time
        self.running = True

    def run(self):
        while self.running:
            try:
                logging.info("Waiting for next task...")
                # This will block if queue is empty
                task = self.queue.get(timeout=2.0)

                # Calculate time spent in queue
                queue_time = (datetime.now() - task.created_at).total_seconds()
                logging.info(f"Got task {task.id} (spent {queue_time:.1f}s in queue)")

                # Simulate processing
                time.sleep(self.process_time)
                logging.info(f"Finished processing task {task.id}")

                self.queue.task_done()

            except queue.Empty:
                logging.info("Queue is empty, waiting for more tasks...")

    def stop(self):
        self.running = False


def demonstrate_blocking():
    # Create a small queue to demonstrate blocking
    task_queue = queue.Queue(maxsize=3)  # Only holds 3 items

    # Create producer that generates 10 tasks
    producer = Producer(task_queue, max_tasks=10)

    # Create slow consumer (takes 2 seconds per task)
    consumer = Consumer(task_queue, process_time=2.0)

    try:
        # Start time tracking
        start_time = time.time()

        # Start threads
        consumer.start()

        logging.info("-" * 50)
        logging.info("Starting producer (queue size = 3, tasks = 10)")
        logging.info("Consumer takes 2 seconds per task")
        logging.info("-" * 50)

        producer.start()

        # Wait for producer to finish
        producer.join()

        # Wait for queue to be empty
        task_queue.join()

        elapsed = time.time() - start_time
        logging.info(f"All tasks completed in {elapsed:.1f} seconds")

    finally:
        # Stop consumer
        consumer.stop()
        consumer.join()


def demonstrate_nonblocking():
    logging.info("\nDemonstrating non-blocking behavior...\n")

    # Create a small queue
    task_queue = queue.Queue(maxsize=3)

    # Try to add items without blocking
    for i in range(5):
        try:
            # put_nowait() raises queue.Full if queue is full
            task_queue.put_nowait(Task(id=i))
            logging.info(f"Added task {i} to queue")
        except queue.Full:
            logging.warning(f"Queue full, couldn't add task {i}")

    # Try to get items without blocking
    for _ in range(5):
        try:
            # get_nowait() raises queue.Empty if queue is empty
            task = task_queue.get_nowait()
            logging.info(f"Got task {task.id} from queue")
        except queue.Empty:
            logging.warning("Queue empty, couldn't get task")


if __name__ == "__main__":
    # First demonstrate blocking behavior
    demonstrate_blocking()

    # Then demonstrate non-blocking behavior
    demonstrate_nonblocking()

```

This example demonstrates several important queue behaviors:

1. **Blocking Put Operation**:
   ```python
   self.queue.put(task)  # Blocks when queue is full
   ```
    - When the queue reaches its maximum size (3 in our example)
    - Producer will block until space becomes available
    - Useful for backpressure

2. **Blocking Get Operation**:
   ```python
   task = self.queue.get(timeout=2.0)  # Blocks when queue is empty
   ```
    - Blocks when trying to get from an empty queue
    - Optional timeout parameter
    - Raises `queue.Empty` if timeout occurs

3. **Non-blocking Alternatives**:
   ```python
   # Non-blocking put
   queue.put_nowait(item)  # Raises queue.Full if full
   
   # Non-blocking get
   item = queue.get_nowait()  # Raises queue.Empty if empty
   ```

4. **Queue Size Control**:
   ```python
   # Fixed size queue
   queue.Queue(maxsize=3)  # Queue with maximum 3 items
   
   # Unlimited queue
   queue.Queue()  # No maxsize means unlimited
   ```

Running this example will show:

1. Producer blocks when queue fills up
2. Consumer blocks when waiting for items
3. System naturally handles different production/consumption rates
4. Non-blocking operations raise exceptions instead of waiting

The output will show:

- When producer is blocked waiting to add items
- When consumer is blocked waiting for items
- Time items spend in the queue
- What happens when using non-blocking operations

This blocking behavior is valuable because it:

1. Provides natural backpressure
2. Prevents memory issues from unbounded queues
3. Synchronizes producers and consumers
4. Handles different processing speeds gracefully