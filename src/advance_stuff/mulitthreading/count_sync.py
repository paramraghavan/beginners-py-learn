'''
 time.sleep() can represent any time-consuming blocking function call,
 while asyncio.sleep() is used to stand in for a non-blocking call (but one that also takes some time to complete).

 asyncio.sleep(), is that the surrounding function can temporarily cede control to another function that’s more readily
 able to do something immediately. In contrast, time.sleep() or any other blocking call is incompatible with asynchronous Python code,
 because it will stop everything in its tracks for the duration of the sleep time.
'''


import time

def count():
    print("One")
    time.sleep(1)
    print("Two")

def main():
    for _ in range(3):
        count()

if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")