# A Python program to generate squares from 1
# to infinity using yield and therefore generator

# An infinite generator function that prints
# next square number. It starts with 1
def nextSquare():
    i = 1

    # An Infinite loop to generate squares
    while True:
        yield i * i
        i += 1  # Next execution resumes
        # from this point

def print_square_sequence_upto_given_limit(upper_limit):
    for num in nextSquare():
        if num > upper_limit:
            print(f'Limit reached {num}')
            break;
        print(f'keep going {num}')


if __name__ == '__main__':
    print_square_sequence_upto_given_limit(1000)