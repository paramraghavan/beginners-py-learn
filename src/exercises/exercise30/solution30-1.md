In this example code, job1 will execute every 10 seconds, not every 5 seconds as scheduled. Here's why:

1. Job1 takes 10 seconds to complete
2. The scheduler waits 5 seconds after the previous job finishes
3. Total time between job starts = 10s (execution) + 5s (wait) = 15 seconds

So while it's scheduled for every 5 seconds, the actual interval between job starts will be 15 seconds due to the
blocking nature of the task and the scheduler's behavior.

