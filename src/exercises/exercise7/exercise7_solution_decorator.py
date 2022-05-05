'''
exercise7 solution decorators has 2 functions - small_loop and big_loop
We would like to find out how much each function call takes

Here we use annotations around the method/function, the annotations work as decorators.
Decorator pattern is a design pattern that allows behaviour to be added to an individual object or function without modifying it.
exercise_solution_decorator
'''
import time

'''
For more on decorators see here --> src/advance_stuff/patterns/decorators/decorator.py
'''
def elapsed_time(func):
    def wrapper_function(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time_in_ms = (time.time() - start_time) * 1000
        message = '{:s} function took {:.3f} ms'.format(func.__name__, elapsed_time_in_ms)
        print(message)
        return result
    return wrapper_function

@elapsed_time
def small_loop():
    return loop(20000)

@elapsed_time
def big_loop():
    return loop(100000)

def loop(loop_count):
    return "-".join(str(i) for i in range(loop_count))

def call():
    small_loop()
    big_loop()

if __name__ == '__main__':
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    call()
    profiler.disable()
    # Export profiler output to file
    stats = pstats.Stats(profiler)
    stats.dump_stats('test.pstat')