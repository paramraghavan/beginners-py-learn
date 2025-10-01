A **Lock** in Python is a synchronization primitive that prevents multiple threads from accessing shared resources simultaneously, avoiding race conditions.

## Why You Need Locks

When multiple threads modify shared data concurrently, you can get unpredictable results. For example, if two threads both read a counter value of 5, increment it, and write back 6, you've lost an increment - the counter should be 7.

## How to Use Lock

Python's `threading.Lock()` has two main methods:
- `acquire()` - blocks until the lock is available, then locks it
- `release()` - unlocks it so other threads can acquire it

Here's a basic example:

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        lock.acquire()
        counter += 1
        lock.release()

threads = [threading.Thread(target=increment) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(counter)  # Will be 500000 (correct!)
```

Without the lock, the final counter value would be unpredictable and usually less than 500000.

## Better Practice: Using Context Manager

Instead of manually acquiring and releasing, use the `with` statement to ensure the lock is always released, even if an exception occurs:

```python
def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1
```

This is safer because the lock automatically releases when the `with` block exits.

## Key Points

- Only one thread can hold a lock at a time
- Other threads trying to acquire it will block (wait) until it's released
- Always release locks you acquire to prevent deadlocks
- Keep the locked section as short as possible to minimize blocking

# RLock, Semaphore, or Event
# Python Threading Primitives

Here are the main synchronization tools beyond basic Lock:

## RLock (Reentrant Lock)

An **RLock** allows the same thread to acquire the lock multiple times without blocking itself. You must release it the same number of times you acquired it.

```python
import threading

rlock = threading.RLock()

def recursive_function(n):
    with rlock:
        print(f"Level {n}")
        if n > 0:
            recursive_function(n - 1)  # Can acquire again!

threading.Thread(target=recursive_function, args=(3,)).start()
```

**Use case:** When a thread needs to call multiple methods that each need the same lock, or for recursive functions.

## Semaphore

A **Semaphore** allows a fixed number of threads to access a resource simultaneously. Think of it as a lock with a counter.

```python
import threading
import time

# Allow max 3 threads to access at once
semaphore = threading.Semaphore(3)

def access_resource(thread_id):
    with semaphore:
        print(f"Thread {thread_id} accessing resource")
        time.sleep(2)
        print(f"Thread {thread_id} done")

threads = [threading.Thread(target=access_resource, args=(i,)) for i in range(10)]
for t in threads: t.start()
```

**Use case:** Limiting concurrent connections to a database, API rate limiting, or managing a pool of resources.

## BoundedSemaphore

Like Semaphore, but raises an error if you release more times than you acquired. It's safer because it catches bugs.

```python
semaphore = threading.BoundedSemaphore(2)
semaphore.release()  # ValueError! Can't release more than initial value
```

## Event

An **Event** lets one or more threads wait until another thread signals them. It's like a flag that starts as False.

```python
import threading
import time

event = threading.Event()

def waiter():
    print("Waiting for event...")
    event.wait()  # Blocks until event is set
    print("Event received! Proceeding.")

def setter():
    time.sleep(2)
    print("Setting event")
    event.set()  # Wakes up all waiting threads

threading.Thread(target=waiter).start()
threading.Thread(target=waiter).start()
threading.Thread(target=setter).start()
```

**Methods:**
- `wait()` - block until the event is set
- `set()` - set the flag to True, waking all waiting threads
- `clear()` - reset the flag to False
- `is_set()` - check if the flag is True

**Use case:** Starting workers after initialization completes, or shutting down threads gracefully.

## Condition

A **Condition** combines a lock with the ability to wait for notifications. It's more advanced than Event.

```python
import threading
import time

condition = threading.Condition()
queue = []

def producer():
    for i in range(5):
        time.sleep(1)
        with condition:
            queue.append(i)
            print(f"Produced {i}")
            condition.notify()  # Wake up one waiting thread

def consumer():
    while True:
        with condition:
            while not queue:  # Wait while queue is empty
                condition.wait()
            item = queue.pop(0)
            print(f"Consumed {item}")
            if item == 4:
                break

threading.Thread(target=producer).start()
threading.Thread(target=consumer).start()
```

**Methods:**
- `wait()` - release lock and wait for notification
- `notify(n=1)` - wake up n waiting threads
- `notify_all()` - wake up all waiting threads

**Use case:** Producer-consumer patterns, complex coordination between threads.

## Barrier

A **Barrier** makes threads wait until a certain number of them reach a synchronization point, then they all proceed together.

```python
import threading
import time
import random

barrier = threading.Barrier(3)  # Wait for 3 threads

def worker(thread_id):
    print(f"Thread {thread_id} doing work...")
    time.sleep(random.uniform(0.5, 2))
    print(f"Thread {thread_id} waiting at barrier")
    
    barrier.wait()  # Block until all 3 threads arrive
    
    print(f"Thread {thread_id} passed barrier!")

for i in range(3):
    threading.Thread(target=worker, args=(i,)).start()
```

**Use case:** Parallel algorithms where threads must synchronize at certain stages, like simulations or parallel computations.

## Quick Comparison

| Primitive | Purpose | Max Waiting Threads |
|-----------|---------|---------------------|
| **Lock** | Mutual exclusion | Unlimited (1 can enter) |
| **RLock** | Reentrant mutual exclusion | Unlimited (1 can enter multiple times) |
| **Semaphore** | Limit concurrent access | Unlimited (N can enter) |
| **Event** | Signal/notification | Unlimited (all notified) |
| **Condition** | Complex wait/notify | Unlimited |
| **Barrier** | Synchronization point | Exact number required |
