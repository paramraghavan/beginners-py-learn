# Function for nth Fibonacci number
# REcursive implementation
# Fibonacci sequence is as follows: f1=1,f2=1,f3=2,f4=3,f5=5,f6=8,f7=13,f8=21,f9=34
def Fibonacci(n):
    if n < 0:
        print("Incorrect input")
        return

    if n == 0:
        return 0

    # Check if n is 1,2,  return 1
    if n == 1 or n == 2:
        return 1

    return Fibonacci(n - 1) + Fibonacci(n - 2)

# Function for nth Fibonacci number
# Non REcursive/Iterative implementation
def nr_Fibonacci(n):
    if n < 0:
        print("Incorrect input")
        return

    if n == 0:
        return 0

    # Check if n is 1,2,  return 1
    if n == 1 or n == 2:
        return 1

    if n == 3 :
        return 2

    prev_minus_1 = 1
    prev = 2
    for i in range(4,n+1,1):
        curr = prev + prev_minus_1
        prev_minus_1 = prev
        prev = curr

    return curr

num = 9

# Driver Program
print(f'Recursive {Fibonacci(num)}')
# Driver Program
print(f'Iterarive {nr_Fibonacci(num)}')