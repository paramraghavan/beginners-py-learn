Examples of using Events and Semaphores in Python. These are powerful
synchronization primitives that can help manage concurrent operations in different scenarios.

Let's start with an Event example, followed by a Semaphore example.

1. Event Example:
   Events are useful for signaling between threads. One thread can wait for a signal, while another thread can send that
   signal.

```python
import threading
import time
import random

# Create an event object
data_ready = threading.Event()


def data_producer():
    print("Producer: Starting")
    time.sleep(random.randint(1, 5))  # Simulate some work
    print("Producer: Data is ready")
    data_ready.set()  # Set the event


def data_consumer():
    print("Consumer: Waiting for data")
    data_ready.wait()  # Wait for the event to be set
    print("Consumer: Data received, starting processing")


# Create and start threads
producer = threading.Thread(target=data_producer)
consumer = threading.Thread(target=data_consumer)

producer.start()
consumer.start()

producer.join()
consumer.join()

print("Main: All done")
```

In this example:

- The producer simulates work, then signals that data is ready using `data_ready.set()`.
- The consumer waits for this signal using `data_ready.wait()` before proceeding.
- This ensures the consumer doesn't try to process data before it's ready.

2. Semaphore Example:
   Semaphores are used to limit the number of threads that can access a resource or perform an operation simultaneously.

```python
import threading
import time
import random

# Create a semaphore that allows 3 threads at a time
pool_sema = threading.Semaphore(value=3)


def worker(id):
    print(f"Worker {id}: Waiting to join the pool")
    with pool_sema:
        print(f"Worker {id}: Entered the pool")
        time.sleep(random.randint(1, 5))  # Simulate some work
        print(f"Worker {id}: Finished and leaving the pool")


# Create and start 10 worker threads
workers = []
for i in range(10):
    worker_thread = threading.Thread(target=worker, args=(i,))
    workers.append(worker_thread)
    worker_thread.start()

# Wait for all workers to finish
for w in workers:
    w.join()

print("Main: All workers have finished")
```

In this example:

- We create a semaphore that allows up to 3 threads to enter the "pool" at once.
- 10 worker threads are created, each trying to enter the pool.
- The semaphore ensures that only 3 workers can be in the pool at any given time.
- When a worker finishes and leaves the pool, it releases the semaphore, allowing another waiting worker to enter.

Both of these examples demonstrate how Events and Semaphores can be used to coordinate between threads:

- Events are great for signaling state changes or completion of tasks.
- Semaphores are excellent for controlling access to limited resources or managing concurrency levels.

These primitives can be very useful in more complex scenarios, such as producer-consumer problems, managing connection
pools, or implementing workflows with dependencies between tasks.

Would you like me to explain any specific aspect of these examples in more detail, or perhaps show how they might be
used in a more complex scenario?