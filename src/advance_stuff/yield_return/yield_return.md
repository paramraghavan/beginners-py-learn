# Yield
The yield statement suspends function’s execution and sends a value back to the caller, 
but retains enough state to enable function to resume where it is left off. When resumed, 
the function continues execution immediately after the last yield run. This allows 
its code to produce a series of values over time, rather than computing them at once 
and sending them back like a list.

# Difference between Python yield and Return

|YIELD|	RETURN|
|------|:-------:|
|Yield is generally used to convert a regular Python function into a generator|	Return is generally used for the end of the execution and “returns” the result to the caller statement.  |
|It replace the return of a function to suspend its execution without destroying local variables.|	It exits from a function and handing back a value to its caller.                      |
|It is used when the generator returns an intermediate result to the caller.|	It is used when a function is ready to send a value.                                                       |
|Code written after yield statement execute in next function call.|	while, code written after return statement wont execute.                                                                |
|It can run multiple times.|	It only runs single time.                                                                                                                                    |
|Yield statement function is executed from the last state from where the function get paused.|	Every function calls run the function from the start.                                         |

Simply put, yield gives you a generator. You'd use it where you would normally use a return in a function. 
 

Reference:
https://www.geeksforgeeks.org/difference-between-yield-and-return-in-python/
