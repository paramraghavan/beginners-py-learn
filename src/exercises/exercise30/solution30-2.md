# How can i run above example as scheduled every 5 seconds


## Using Threading with Schedule:

```python
import schedule
import time
from threading import Thread


def job1():
    print("Starting job1")
    time.sleep(10)  # Simulate a long-running task
    print("Finished job1")


# Run the job in a separate thread
def run_threaded(job_func):
    job_thread = Thread(target=job_func)
    job_thread.start()


# Schedule the job to run in a thread
schedule.every(5).seconds.do(run_threaded, job1)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## For better control and modern Python practices, using asyncio. Here's a more robust solution:

```python
import asyncio
import time
from datetime import datetime


async def job1():
    print(f"Starting job1 at {datetime.now()}")
    # Simulate a long-running task using asyncio.sleep
    await asyncio.sleep(10)
    print(f"Finished job1 at {datetime.now()}")


async def schedule_task():
    while True:
        # Create a task for job1
        asyncio.create_task(job1())
        # Wait 5 seconds before scheduling the next one
        await asyncio.sleep(5)


# Run the scheduler
asyncio.run(schedule_task())
```

The asyncio version has several advantages:

1. Better control over concurrent execution
2. More accurate timing
3. More efficient resource usage
4. Easier to manage multiple scheduled tasks

## Little more complicated Another way that handles multiple jobs and graceful shutdown:

```python
import asyncio
import signal
from datetime import datetime


class JobScheduler:
    def __init__(self):
        self.running = True
        self.tasks = set()

    async def job1(self):
        print(f"Starting job1 at {datetime.now()}")
        await asyncio.sleep(10)  # Simulate long-running task
        print(f"Finished job1 at {datetime.now()}")

    async def schedule_jobs(self):
        while self.running:
            # Create and track the task
            task = asyncio.create_task(self.job1())
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)

            await asyncio.sleep(5)  # Wait for next schedule

    async def shutdown(self):
        self.running = False
        # Wait for all running tasks to complete
        if self.tasks:
            await asyncio.gather(*self.tasks)


def handle_shutdown(scheduler, loop):
    loop.create_task(scheduler.shutdown())


async def main():
    scheduler = JobScheduler()
    loop = asyncio.get_running_loop()

    # Setup signal handlers for graceful shutdown
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda: handle_shutdown(scheduler, loop)
        )

    await scheduler.schedule_jobs()


if __name__ == "__main__":
    asyncio.run(main())
```

This final version includes:

- Proper task tracking and cleanup
- Signal handling for graceful shutdown
- Clear separation of concerns
- Easy addition of new scheduled jobs

Overall the first ones seems to be the simplest