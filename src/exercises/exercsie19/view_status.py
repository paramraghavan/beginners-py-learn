from multiprocessing import Manager
from shared_file_state import get_shared_dict, print_complete_status

if __name__ == "__main__":
    # Create a new manager to connect to the shared memory
    manager = Manager()

    # Get the shared dictionary
    file_status_map = get_shared_dict()

    # If the dictionary is empty, it might mean the main script isn't running
    if not file_status_map:
        print("The shared dictionary is empty. Make sure the main script is running.")
    else:
        print_complete_status(file_status_map)