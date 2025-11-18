import pickle
import os
import signal
import sys
import atexit
import tempfile

DICT_PATH = 'state.pickle'

def save_state(d):
    """
    Atomically saves the given dictionary to DICT_PATH.
    """
    fd, tmp_name = tempfile.mkstemp(prefix='state.', suffix='.tmp', dir='.')
    try:
        with os.fdopen(fd, 'wb') as f:
            pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, DICT_PATH)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise

def load_state():
    """
    Loads and returns dictionary from DICT_PATH, or empty dict if file doesn't exist.
    """
    if os.path.exists(DICT_PATH):
        with open(DICT_PATH, 'rb') as f:
            return pickle.load(f)
    return {}

def handle_exit(signum, frame):
    """
    Signal handler that saves current state and exits gracefully.
    """
    print(f"Received signal {signum}, saving state and exiting.")
    save_state(my_dict)
    sys.exit(0)

def main():
    global my_dict
    # Restore previous state
    my_dict = load_state()
    print("Loaded dict:", my_dict)
    # Example usage
    my_dict['counter'] = my_dict.get('counter', 0) + 1
    print("Updated dict:", my_dict)
    save_state(my_dict)  # Explicit save (atexit and signal will also handle)

if __name__ == "__main__":
    my_dict = {}

    # Register signal handlers
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    # Register atexit handler
    atexit.register(lambda: save_state(my_dict))

    main()
