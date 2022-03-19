'''
exercise7 solution has 2 functions - small_loop and big_loop
We would like to find out how much each function call takes

'''
from typing import List, Any, Union

def loop(loop_count):
    return "-".join(str(i) for i in range(loop_count))

def small_loop():
    return loop(20000)

def big_loop():
    return loop(100000)



def measure_invocation_time():
    import time
    start_time = time.time()
    small_loop()
    elapsed_time_in_ms = (time.time() - start_time)*1000

    start_time_alt = time.time()
    big_loop()
    elapsed_time_alt_in_ms = (time.time() - start_time_alt)*1000

    print('{:s} function took {:.3f} ms'.format(small_loop.__name__, elapsed_time_in_ms))
    print('{:s} function took {:.3f} ms'.format(big_loop.__name__, elapsed_time_alt_in_ms))



if __name__ == '__main__':
    measure_invocation_time()

