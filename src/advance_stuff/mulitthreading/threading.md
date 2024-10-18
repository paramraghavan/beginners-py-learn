2. `threading` module:

The `threading` module is part of Python's standard library and is used for creating and managing threads, allowing
concurrent execution of code.

Key features:

- Create and start new threads
- Synchronize threads using locks, events, and semaphores
- Share data between threads safely

Here's a simple example:

```python
import threading
import time


def worker(name):
    print(f"Worker {name} started")
    time.sleep(2)
    print(f"Worker {name} finished")


threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All workers finished")
```
