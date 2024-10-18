Synchronization in Python is important when multiple threads access shared resources to prevent race
conditions and ensure data consistency. Python provides several synchronization primitives through the `threading`
module. 


1. **Lock (Mutex):**
   A basic synchronization primitive that allows only one thread to enter the locked code at a time.

```python
import threading

lock = threading.Lock()


def synchronized_function():
    with lock:
        # Critical section
        print("This will only execute one at a time")
```

2. **RLock (Reentrant Lock):**
   Similar to Lock, but can be acquired multiple times by the same thread.

```python
rlock = threading.RLock()


def reentrant_function():
    with rlock:
        # Can be called multiple times by the same thread
        print("This is reentrant")
        reentrant_function()  # This won't deadlock
```

3. **Semaphore:**
   Allows a limited number of threads to access a resource.

```python
semaphore = threading.Semaphore(2)  # Allow 2 threads at a time


def limited_concurrency():
    with semaphore:
        print("Only 2 threads can execute this simultaneously")
```

4. **Event:**
   Used for signaling between threads.

```python
event = threading.Event()


def waiter():
    print("Waiting for event")
    event.wait()
    print("Event received!")


def signaler():
    print("About to set event")
    event.set()


# In main thread:
threading.Thread(target=waiter).start()
threading.Thread(target=signaler).start()
```

5. **Condition:**
   Allows threads to wait for a certain condition to become true.

```python
condition = threading.Condition()
data_ready = False


def consumer():
    with condition:
        while not data_ready:
            condition.wait()
        print("Data consumed")


def producer():
    global data_ready
    with condition:
        data_ready = True
        condition.notify()


# In main thread:
threading.Thread(target=consumer).start()
threading.Thread(target=producer).start()
```

6. **Queue:**
   A thread-safe way to exchange data between threads.

```python
from queue import Queue

q = Queue()


def producer():
    q.put("Data")


def consumer():
    data = q.get()
    print(f"Received: {data}")


# In main thread:
threading.Thread(target=producer).start()
threading.Thread(target=consumer).start()
```

Here's a more complete example combining some of these concepts:

```python
import threading
import time
import random
from queue import Queue

# Shared resources
buffer = Queue(maxsize=5)
lock = threading.Lock()


def producer(id):
    while True:
        item = random.randint(1, 100)
        buffer.put(item)
        with lock:
            print(f"Producer {id} added {item}. Buffer size: {buffer.qsize()}")
        time.sleep(random.random())


def consumer(id):
    while True:
        item = buffer.get()
        with lock:
            print(f"Consumer {id} removed {item}. Buffer size: {buffer.qsize()}")
        buffer.task_done()
        time.sleep(random.random())


# Create threads
producers = [threading.Thread(target=producer, args=(i,)) for i in range(2)]
consumers = [threading.Thread(target=consumer, args=(i,)) for i in range(3)]

# Start threads
for t in producers + consumers:
    t.daemon = True  # Allow the program to exit even if threads are running
    t.start()

# Run for a while
time.sleep(10)
print("Finished")
```

This example demonstrates:

- Using a Queue for thread-safe data exchange
- Using a Lock to synchronize access to shared output
- Creating multiple producer and consumer threads

It is important to design your multithreaded programs carefully to avoid deadlocks and ensure efficient operation.
