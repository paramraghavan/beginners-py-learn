# Using Python's built-in debugger (pdb) 

1. **Import pdb module**: First, you need to import the pdb module into your script.
```python
import pdb
```
2. **Set a breakpoint**: To stop the execution of your code at a specific point, insert the line pdb.set_trace() at that
   point in your code.
```python
pdb.set_trace()
```
3. **Run your script**: When you run your script, it will halt execution at the point where you inserted the
   pdb.set_trace() line.
4. **Navigate through the debugger:**
```text
Basic Commands:
    c (continue): Continue execution until the next breakpoint.
    n (next): Continue execution until the next line of the current function.
    s (step): Step into functions.
Inspect Variables:
    Typing the name of a variable will display its current value.
Manipulate Execution:
    q (quit): Quit the debugger and the program.
    l (list): Show the current position in the file.
Stack Inspection:
    w (where): Show the current stack trace with lines of code.
Conditional Breakpoints:
    You can set breakpoints conditionally using Python expressions.
Post-mortem Debugging:
    You can also use pdb to debug a script after it has encountered an exception by running python -m pdb your_script.py.
Exiting the Debugger:
    Once you are done debugging, you can exit the debugger by typing q or using the exit() command.
```
5. When you run this script,[sample_debug.py](sample_debug.py), it will stop at the pdb.set_trace() line, and you can use pdb commands to inspect
   variables, step through the code, and diagnose any issues. 