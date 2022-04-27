numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# returns True if number is even
def check_multiples_of_three(number):
    if number % 3 == 0:
          return True

    return False

# Extract elements from the numbers list for which check_even() returns True
even_numbers_iterator = filter(check_multiples_of_three, numbers)

# converting to list
even_numbers = list(even_numbers_iterator)

#
# returns Output: [2, 4, 6, 8, 10]
#
print(even_numbers)
