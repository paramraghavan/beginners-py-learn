'''
List the current thread and process id
'''
import os
# Get the process ID of
# the current process
pid = os.getpid()
# Print the process ID of
# the current process
print(pid)
import threading
print(threading.current_thread().name)
'''
get_ident() is an inbuilt method of the threading module in Python. It is used to return the
 "thread identifier" of the current thread. Thread identifiers can be recycled when a thread 
 exits and another thread is created. The value has no direct meaning.
'''
print(threading.get_ident())

print(80*'=')
''''
List the threads associated with the current process id
pip install psutil
'''
import psutil

current_process = psutil.Process()
print(f'Parent process: {current_process}')
children = current_process.children(recursive=True)
count_child_threads = 0
for child in children:
    print('Child pid is {}'.format(child.pid))
    count_child_threads +=1
if count_child_threads == 0:
    print('No child threads associated')
else:
    print(f'{count_child_threads} child threads associated')
print(80*'=')