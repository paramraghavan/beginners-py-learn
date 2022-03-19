<pre>
exercise7 solution has 2 functions - small_loop and big_loop
We would like to find out how much each function call takes


def loop(loop_count):
    return "-".join(str(i) for i in range(loop_count))

def small_loop():
    return loop(10000)

def big_loop():
    return loop(100000)


</pre>


