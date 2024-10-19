Example showing the usage of shared memory for a dictionary across multiple Python scripts. Let's create a simple task management
system where different scripts can add, update, and view tasks in a shared dictionary.

## shared_task_manager.py

```python
# this keeps running, shared_task_manager.py
from multiprocessing import Manager, Process
import time

def create_shared_dict():
    manager = Manager()
    return manager.dict()

def add_task(tasks, task_id, description):
    tasks[task_id] = {"description": description, "status": "pending"}
    print(f"Added task {task_id}: {description}")

def update_task_status(tasks, task_id, status):
    if task_id in tasks:
        tasks[task_id]["status"] = status
        print(f"Updated task {task_id} status to: {status}")
    else:
        print(f"Task {task_id} not found")

def view_tasks(tasks):
    print("\nCurrent Tasks:")
    for task_id, task_info in tasks.items():
        print(f"Task {task_id}: {task_info['description']} - Status: {task_info['status']}")

if __name__ == "__main__":
    shared_tasks = create_shared_dict()
    
    # Initialize with some tasks
    add_task(shared_tasks, 1, "Implement login functionality")
    add_task(shared_tasks, 2, "Design database schema")
    
    view_tasks(shared_tasks)

    # Keep the script running to allow other scripts to connect
    print("\nShared task manager is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShared task manager stopped.")
```

## add_task_script.py

```python
from shared_task_manager import create_shared_dict, add_task, view_tasks
import time

if __name__ == "__main__":
    shared_tasks = create_shared_dict()
    time.sleep(1)  # Wait for the main script to initialize

    add_task(shared_tasks, 3, "Implement user authentication")
    add_task(shared_tasks, 4, "Create API documentation")
    
    view_tasks(shared_tasks)
```

## update_task_script.py
```python
from shared_task_manager import create_shared_dict, update_task_status, view_tasks
import time

if __name__ == "__main__":
    shared_tasks = create_shared_dict()
    time.sleep(1)  # Wait for the main script to initialize

    update_task_status(shared_tasks, 1, "completed")
    update_task_status(shared_tasks, 3, "in progress")
    
    view_tasks(shared_tasks)
```

## view_tasks_script.py

```python
from shared_task_manager import create_shared_dict, view_tasks
import time

if __name__ == "__main__":
    shared_tasks = create_shared_dict()
    time.sleep(1)  # Wait for the main script to initialize

    view_tasks(shared_tasks)

```

### This  example creates a simple task management system using a shared dictionary. Here's how to use it:

1. Save the code in four separate files: `shared_task_manager.py`, `add_task_script.py`, `update_task_script.py`, and
   `view_tasks_script.py`.

2. Run `shared_task_manager.py` first. This will create the shared dictionary, initialize it with some tasks, and keep
   running to allow other scripts to connect.

3. In separate terminal windows, you can now run the other scripts:
    - Run `add_task_script.py` to add new tasks to the shared dictionary.
    - Run `update_task_script.py` to update the status of existing tasks.
    - Run `view_tasks_script.py` to view all current tasks in the shared dictionary.

4. You'll see that all scripts can access and modify the same shared dictionary of tasks.

Key improvements in this example:

1. More practical use case: A task management system that multiple scripts can interact with.
2. Clear separation of concerns: Different scripts for adding tasks, updating tasks, and viewing tasks.
3. Continuous running of the main script: Allows other scripts to connect at any time.
4. Better demonstration of shared state: You can see how changes made by one script are immediately visible to others.

To use this system:

1. Start `shared_task_manager.py` and keep it running.
2. Run `add_task_script.py` to add new tasks.
3. Run `update_task_script.py` to change the status of some tasks.
4. Run `view_tasks_script.py` at any point to see the current state of all tasks.
