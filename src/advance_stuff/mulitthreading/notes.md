# Concurrent Parallel and Asynchronous methods
- **Concurrency** is when the execution of multiple tasks is interleaved, instead of each task being executed sequentially one after another.
- **Parallelism** is when these tasks are actually being executed in parallel.
-![image](https://user-images.githubusercontent.com/52529498/145838588-779a071f-1d28-4fd1-a5c7-d025dca96ba8.png)
- **Asynchrony** is a separate concept (even though related in some contexts). It refers to the fact that one event might be happening at a different time (not in synchrony) to another event. The below diagrams illustrate what's the difference between a synchronous and an asynchronous execution, where the actors can correspond to different threads, processes or even servers.

- ![image](https://user-images.githubusercontent.com/52529498/145838828-24605398-03ad-46b8-bb1f-a59aeec2e056.png)
- ![image](https://user-images.githubusercontent.com/52529498/145838855-0296111a-a567-4adb-97a4-428311c8d3dc.png)

# asyncio.gather is like Future  or Callable in java
 When working with multiple coroutines and you want to wait for all of them to complete, you can use the asyncio.gather() function. 
 This function is a part of the asyncio library, which is designed for writing concurrent code using the async/await syntax.
```python
import asyncio

async def my_coroutine(id, delay):
    print(f"Coroutine {id} starting")
    await asyncio.sleep(delay)
    print(f"Coroutine {id} finished")
    return f"Result from coroutine {id}"

async def main():
    # List of coroutines
    tasks = [my_coroutine(1, 2), my_coroutine(2, 1), my_coroutine(3, 3)]

    # Waiting for all coroutines to complete
    results = await asyncio.gather(*tasks)

    # Print results
    for result in results:
        print(result)

# Run the main coroutine
asyncio.run(main())

```
# References 
- https://stackoverflow.com/questions/4844637/what-is-the-difference-between-concurrency-parallelism-and-asynchronous-methods
- https://medium.com/@sh.hooshyari/introduction-to-asyncio-in-python-36983d6a715a