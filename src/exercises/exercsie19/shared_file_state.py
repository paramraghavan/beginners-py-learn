from multiprocessing import Manager, freeze_support
import time

global_file_status_map = None

def get_shared_dict():
    global global_file_status_map

    return global_file_status_map

def add_file_status(file_status_map, filename, status):
     file_status_map[filename] = {'filename': filename, 'status': status}

def update_file_status(file_status_map, filename, status):
    if filename in file_status_map:
        file_status_map[filename]['status'] = status
    else:
        file_status_map[filename] = {'filename': filename, 'status': status}

def get_file_status(file_status_map, filename):
    return file_status_map.get(filename, {}).get('status', 'unknown')

def print_complete_status(file_status_map):
    print(80*'*')
    for key, value in file_status_map.items():
        print(f"Filename: {key}, Status: {value['status']}")
    print(80 * '*')

if __name__ == "__main__":
    freeze_support()  # Add this line
    manager = Manager()
    global_file_status_map = manager.dict()

    shared_tasks = get_shared_dict()

    # Initialize with some tasks
    add_file_status(shared_tasks, '1', "open")
    add_file_status(shared_tasks, '2', "open")

    get_file_status(shared_tasks, '1')
    print_complete_status(shared_tasks)
    # Keep the script running to allow other scripts to connect
    print("\nShared task manager is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nShared task manager stopped.")