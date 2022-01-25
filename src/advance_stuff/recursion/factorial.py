# Python 3 program to find
# factorial of given number
# recursive
def factorial(n):
    if n == 1 or n == 0:
        return 1

    return n * factorial(n - 1);


# Driver Code
num = 5;
print("Factorial of", num, "is",
factorial(num))

# recursive
def nr_factorial(n):
    if n == 1 or n == 0:
        return 1

    result =1
    for i in range(2, n+1,1):
        result *= i
    return result

# Driver Code
num = 5;
print("Non Recursive Factorial of", num, "is",
nr_factorial(num))