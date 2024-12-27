Using the `schedule` and `threading` modules in Python. These modules are useful for task
scheduling and concurrent execution. 

1. `schedule` module:

The `schedule` module is not part of Python's standard library, but it's a popular third-party module for task
scheduling. It allows you to schedule tasks to run at specific times or intervals.

Key features:

- Schedule functions to run at fixed intervals
- Run jobs on specific days or dates
- Cancel scheduled jobs

Here's a simple example:

my_job(), this is the task we'll be scheduling to run at various times.
This script sets up three different schedules for the my_job() function:
- Every 10 minutes
- Every hour
- Every day at 10:30 AM

## While loop

This is an infinite loop that keeps the program running and checking for scheduled tasks:

- schedule.run_pending() checks the scheduled tasks and runs any that are due.
- time.sleep(1) makes the program wait for 1 second before the next check. This prevents the program from constantly
  using CPU resources.

```python
import schedule
import time


def my_job():
    print("I'm working...")


schedule.every(10).minutes.do(my_job)
schedule.every().hour.do(my_job)
schedule.every().day.at("10:30").do(my_job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## what happens if i change the time.sleep from 1 to 300
Here's the explanation:

1. Sleep duration:
   `time.sleep(300)` means the program will sleep for 300 seconds (5 minutes) between checks.

2. Worst-case scenario:
   Imagine the following sequence of events:

    - At 10:29:59, the program checks for pending tasks.
    - Finding no tasks due yet, it goes to sleep for 5 minutes.
    - The program will wake up at 10:34:59.

3. Missed window:
    - During the sleep period, the scheduled time (10:30:00) passes.
    - The program is unaware of this while it's sleeping.

4. Next check:
    - When the program wakes up at 10:34:59, it immediately checks for pending tasks.
    - It finds that the 10:30:00 task is overdue and runs it right away.

5. Timing precision:
    - In this worst case, the task runs 4 minutes and 59 seconds later than scheduled.
    - This is just 1 second shy of the full 5-minute sleep duration.

6. Variable delay:
    - The actual delay could be anywhere from 0 to 299 seconds, depending on when the last check occurred relative to
      the scheduled time.

By increasing the sleep duration, we reduce CPU usage, but we also introduce the possibility of tasks running later than
their exact scheduled times.

For many applications, this level of imprecision is acceptable. However, if exact timing is crucial, you'd need to
reduce the sleep duration.

## The schedule jobs are run sequentially

Yes, the schedule jobs are run sequentially. 
1. Sequential execution:
   - When `schedule.run_pending()` is called, it checks all scheduled jobs.
   - If multiple jobs are due to run at the same time, they are executed one after another, not concurrently.

2. Order of execution:
   - Jobs are typically executed in the order they were added to the scheduler.
   - However, the exact order isn't guaranteed, especially for jobs scheduled at the same time.

3. Blocking nature:
   - Each job blocks the execution of subsequent jobs until it completes.
   - If one job takes a long time to run, it will delay the start of other due jobs.

4. Implications:
   - For short-running tasks, this sequential execution is usually not a problem.
   - For longer-running tasks, it can lead to delays and timing issues.

Here's an example to illustrate this:

```python
import schedule
import time

def job1():
    print("Starting job1")
    time.sleep(10)  # Simulate a long-running task
    print("Finished job1")

def job2():
    print("Running job2")

schedule.every(5).seconds.do(job1)
schedule.every(5).seconds.do(job2)

while True:
    schedule.run_pending()
    time.sleep(1)
```

In this scenario:

- Both `job1` and `job2` are scheduled to run every 5 seconds.
- `job1` takes 10 seconds to complete.
- You'll observe that `job2` doesn't run exactly every 5 seconds. It will often be delayed because it waits for `job1`
  to finish.

**To handle concurrent execution of jobs, you would need to combine the `schedule` module with something like the
`threading` module. This way, each job could run in its own thread, allowing for parallel execution.**

## Schedule and Threading together

Combining the `schedule` module with `threading` to allow concurrent execution of scheduled jobs, particularly useful
when you have long-running tasks that shouldn't block other scheduled jobs.

Here's an example that demonstrates this:

```python
import schedule
import threading
import time


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def job1():
    print(f"Starting job1 at {time.strftime('%H:%M:%S')}")
    time.sleep(10)  # Simulate a long-running task
    print(f"Finished job1 at {time.strftime('%H:%M:%S')}")


def job2():
    print(f"Running job2 at {time.strftime('%H:%M:%S')}")


# Schedule jobs
schedule.every(5).seconds.do(run_threaded, job1)
schedule.every(5).seconds.do(run_threaded, job2)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
```

Let's break down this code:

1. We define a `run_threaded` function that takes a job function as an argument and runs it in a new thread.

2. We define two job functions: `job1` (a long-running task) and `job2` (a quick task).

3. Instead of scheduling `job1` and `job2` directly, we schedule `run_threaded(job1)` and `run_threaded(job2)`. This
   means each job will be started in its own thread when it's time to run.

4. In the main loop, we still use `schedule.run_pending()` to check for due jobs, but now each job starts in its own
   thread.

With this setup:

- `job1` and `job2` will both start every 5 seconds, regardless of how long each takes to complete.
- `job1` can run for 10 seconds without preventing `job2` from starting on time.
- You'll see that `job2` runs every 5 seconds, even while `job1` is still running.

A few important notes:

- This approach is good for I/O-bound tasks but may not improve performance for CPU-bound tasks due to Python's Global
  Interpreter Lock (GIL).
- Be cautious with shared resources. If your jobs access shared data, you may need to implement proper synchronization
  mechanisms.
- For a large number of concurrent tasks, you might want to consider using a thread pool to limit the number of
  simultaneous threads.


