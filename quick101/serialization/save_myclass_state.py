import pickle
import os

"""
Demo class: Contains a picklable value and a non-picklable unpicklable attribute (file handle).
    __getstate__: Excludes unpicklable so pickling doesn't fail.
    __setstate__: Restores everything except the file, setting unpicklable to None.

    Creates the object.
    Saves it to pickle (excluding the file).
    Closes and deletes the object.
    Loads the object; restored data is there except the file handle.
"""
class Demo:
    def __init__(self, value):
        self.value = value
        self.unpicklable = open('test.txt', 'w')  # File objects cannot be pickled

    def __getstate__(self):
        """
        Only save picklable attributes. Exclude 'unpicklable'.
        """
        state = self.__dict__.copy()  # Copy all attributes
        if 'unpicklable' in state:
            del state['unpicklable']
        return state

    def __setstate__(self, state):
        """
        Restore attributes. You can recreate or ignore 'unpicklable'.
        """
        self.__dict__.update(state)
        self.unpicklable = None  # File not reopened; set to None or recreate if needed


def save_demo(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_demo(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def main():
    filename = 'demo.pickle'

    # Create the object
    demo = Demo(42)
    print("Original value:", demo.value)
    print("Original unpicklable:", demo.unpicklable)

    # Save state
    save_demo(demo, filename)
    print("Demo object saved.\n")

    # Clean up: Close file and delete object to show restoration
    demo.unpicklable.close()
    del demo

    # Load state
    loaded = load_demo(filename)
    print("Loaded value:", loaded.value)
    print("Loaded unpicklable:", loaded.unpicklable)  # Will be None per __setstate__


if __name__ == "__main__":
    # Create a dummy file for demonstration
    if not os.path.exists('test.txt'):
        with open('test.txt', 'w') as tf:
            tf.write("hello world")
    main()
