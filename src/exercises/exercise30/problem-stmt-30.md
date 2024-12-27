In the example below:
```python

import schedule
import time

def job1():
    print("Starting job1")
    time.sleep(10)  # Simulate a long-running task
    print("Finished job1")


schedule.every(5).seconds.do(job1)

while True:
    schedule.run_pending()
    time.sleep(1)
```

- JOB1 TAKES 10 SECONDS TO FINISH AND IT I SCHEDULE EVERY 5 MINS HOW OFTEN WILL JOB 1 EXECUTE
- What can I do it make it run as scheduled
