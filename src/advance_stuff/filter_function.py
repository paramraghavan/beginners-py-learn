numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# returns True if number is a multiple of 3
def check_multiples_of_three(number):
    if number % 3 == 0:
          return True

    return False

# Extract elements from the numbers list for which check_multiples_of_three() returns True
multiples_of_three_iterator = filter(check_multiples_of_three, numbers)

# converting to list
multiples_of_three = list(multiples_of_three_iterator)

#
# returns Output: [3, 6, 9]
#
print(multiples_of_three)
